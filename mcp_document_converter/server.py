"""MCP server entry point for doc2md-helper.

Run as: doc2md-helper serve
Communicates via stdio (standard MCP transport), or use
`doc2md-helper serve --http` for Streamable HTTP on localhost (port 5555
by default).
"""

from __future__ import annotations

import asyncio
import logging
import sys
import tempfile
from pathlib import Path

from fastmcp import FastMCP

logger = logging.getLogger(__name__)

_default_repo_root: str | None = None

mcp = FastMCP(
    "doc2md-helper",
    instructions=(
        "Document converter for converting PDF, DOCX, and Excel files to Markdown. "
        "Provides two options for PDF conversion: MarkItDown (fast, text-based PDFs) and "
        "Marker (high-quality OCR, scanned PDFs). For PDF conversion, always ask the user "
        "which option they prefer before proceeding."
    ),
)


def _save_output(markdown_text: str, source_path: Path, output_path: str | None = None) -> Path:
    if output_path:
        dest = Path(output_path).expanduser().resolve()
    else:
        dest = source_path.with_suffix(".md")

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(markdown_text, encoding="utf-8")
    return dest


def _resolve_path(file_path: str) -> Path:
    resolved = Path(file_path).expanduser().resolve()
    return resolved


def _check_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")


def _truncate_output(text: str, max_chars: int = 5000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n...(truncated, total {len(text)} chars)..."


@mcp.tool()
def convert_pdf_with_marker(file_path: str, output_path: str | None = None) -> str:
    """Convert PDF files to Markdown using Marker library (high-quality OCR).
    Best for scanned PDFs or complex layouts. Requires marker-pdf and may be slower.

    IMPORTANT: When a user requests PDF conversion, first ask them whether they want
    "1. Fast, lightweight option (MarkItDown, best for text-based PDFs)" or
    "2. High-quality OCR option (Marker, best for scanned PDFs)".

    Args:
        file_path: Absolute or relative path to PDF file
        output_path: Output Markdown file path (optional, auto-generated if not provided)

    Returns:
        Converted Markdown text content with file save confirmation
    """
    path = _resolve_path(file_path)
    _check_file(path)

    try:
        from mcp_document_converter.pdf2markdown import convert_pdf_page_by_page
    except ImportError as e:
        raise ImportError(
            "marker-pdf not installed. Please install with: "
            "pip install doc2md-helper[marker]"
        ) from e

    with tempfile.TemporaryDirectory() as tmp_dir:
        convert_pdf_page_by_page(str(path), tmp_dir)

        output_files = list(Path(tmp_dir).glob("*.md"))
        if not output_files:
            return "Error: No output generated from PDF conversion"

        combined = [f for f in output_files if "_page_" not in f.name]
        if combined:
            markdown_text = combined[0].read_text(encoding="utf-8")
        else:
            all_content = []
            for f in sorted(output_files):
                all_content.append(f.read_text(encoding="utf-8"))
            markdown_text = "\n\n".join(all_content)

    saved = _save_output(markdown_text, path, output_path)
    result = f"File saved: {saved}\n\n{_truncate_output(markdown_text)}"
    return result


@mcp.tool()
def convert_pdf_with_markitdown(file_path: str, output_path: str | None = None) -> str:
    """Convert PDF files to Markdown using MarkItDown library (fast, lightweight).
    Best for text-based PDFs. No GPU required, fast but limited for scanned documents.

    IMPORTANT: When a user requests PDF conversion, first ask them whether they want
    "1. Fast, lightweight option (MarkItDown, best for text-based PDFs)" or
    "2. High-quality OCR option (Marker, best for scanned PDFs)".

    Args:
        file_path: Absolute or relative path to PDF file
        output_path: Output Markdown file path (optional, auto-generated if not provided)

    Returns:
        Converted Markdown text content with file save confirmation
    """
    path = _resolve_path(file_path)
    _check_file(path)

    from mcp_document_converter.pdf2markdown_markitdown import pdf_to_markdown_simple

    markdown_text = pdf_to_markdown_simple(str(path))
    saved = _save_output(markdown_text, path, output_path)
    result = f"File saved: {saved}\n\n{_truncate_output(markdown_text)}"
    return result


@mcp.tool()
def convert_docx_to_markdown(file_path: str, output_path: str | None = None) -> str:
    """Convert Word documents (.docx / .doc) to Markdown format.
    Supports multiple backends including textract, mammoth, and python-docx.

    Args:
        file_path: Absolute or relative path to Word file
        output_path: Output Markdown file path (optional, auto-generated if not provided)

    Returns:
        Converted Markdown text content with file save confirmation
    """
    path = _resolve_path(file_path)
    _check_file(path)

    from mcp_document_converter.docx2markdown import docx_to_markdown

    with tempfile.TemporaryDirectory() as tmp_dir:
        md_path = docx_to_markdown(str(path), tmp_dir)
        markdown_text = Path(md_path).read_text(encoding="utf-8")

    saved = _save_output(markdown_text, path, output_path)
    result = f"File saved: {saved}\n\n{_truncate_output(markdown_text)}"
    return result


@mcp.tool()
def convert_excel_to_markdown(file_path: str, output_path: str | None = None) -> str:
    """Convert Excel files (.xlsx / .xls) to Markdown format.
    Supports multiple backends including MarkItDown, openpyxl, and pandas.

    Args:
        file_path: Absolute or relative path to Excel file
        output_path: Output Markdown file path (optional, auto-generated if not provided)

    Returns:
        Converted Markdown text content with file save confirmation
    """
    path = _resolve_path(file_path)
    _check_file(path)

    from mcp_document_converter.excel2markdown import excel_to_markdown_simple

    markdown_text = excel_to_markdown_simple(str(path))
    saved = _save_output(markdown_text, path, output_path)
    result = f"File saved: {saved}\n\n{_truncate_output(markdown_text)}"
    return result


def main(
    repo_root: str | None = None,
    transport: str = "stdio",
    host: str | None = None,
    port: int | None = None,
) -> None:
    """Run the MCP server (stdio or HTTP).

    On Windows, Python 3.8+ defaults to `ProactorEventLoop`, which
    can have issues. Switching to `WindowsSelectorEventLoopPolicy`
    before fastmcp starts its loop avoids the deadlock.

    Args:
        repo_root: Default repository root for tool calls
        transport: "stdio" (default) or "streamable-http" for local HTTP
        host: Bind address when using HTTP (required for HTTP)
        port: Port when using HTTP (required for HTTP)
    """
    global _default_repo_root
    if repo_root:
        _default_repo_root = repo_root
    else:
        _default_repo_root = str(Path.cwd())

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if transport == "stdio":
        mcp.run(transport="stdio", show_banner=False)
    elif transport == "streamable-http":
        if host is None or port is None:
            host = host or "127.0.0.1"
            port = port or 5555
        mcp.run(transport="streamable-http", host=host, port=port)
    else:
        raise ValueError(f"Unsupported transport: {transport}")


if __name__ == "__main__":
    main()
