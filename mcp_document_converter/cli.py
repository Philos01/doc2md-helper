"""CLI entry point for doc2md-helper.

Usage:
    doc2md-helper install
    doc2md-helper init
    doc2md-helper serve [--http] [--host HOST] [--port PORT]
    doc2md-helper mcp
    doc2md-helper convert-pdf FILE [--output OUTPUT]
    doc2md-helper convert-pdf-marker FILE [--output OUTPUT]
    doc2md-helper convert-docx FILE [--output OUTPUT]
    doc2md-helper convert-excel FILE [--output OUTPUT]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Windows 终端 UTF-8 编码修复
if sys.platform == "win32" and sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


logger = logging.getLogger(__name__)


def _get_version() -> str:
    """Get the installed package version."""
    try:
        from importlib.metadata import version
        return version("doc2md-helper")
    except Exception:
        return "dev"


def _print_banner() -> None:
    """Print the startup banner."""
    version = _get_version()
    print(f"""
📄 doc2md-helper v{version}

  Document converter for PDF, DOCX, and Excel to Markdown.

  Commands:
    install        Set up MCP server for AI coding platforms
    init           Alias for install
    serve          Start MCP server (stdio by default)
    mcp            Alias for serve
    convert-pdf    Convert PDF to Markdown (MarkItDown - fast)
    convert-pdf-marker  Convert PDF to Markdown (Marker - high quality)
    convert-docx   Convert Word document to Markdown
    convert-excel  Convert Excel to Markdown

  Run doc2md-helper <command> --help for details
""")


def _handle_init(args: argparse.Namespace) -> None:
    """Handle install/init command."""
    from mcp_document_converter.skills import (
        install_platform_configs,
        generate_skills,
        inject_claude_md,
        inject_platform_instructions,
        install_hooks,
    )
    from pathlib import Path

    repo_root = Path.cwd()

    dry_run = getattr(args, "dry_run", False)
    target = getattr(args, "platform", "all") or "all"
    if target == "claude-code":
        target = "claude"

    print("Installing MCP server config...")
    configured = install_platform_configs(repo_root, target=target, dry_run=dry_run)

    if not configured:
        print("No platforms detected or configured.")
    else:
        print(f"\nConfigured {len(configured)} platform(s): {', '.join(configured)}")

    if dry_run:
        print("\n[dry-run] Would complete installation.")
        return

    # Install skills for Claude Code
    if target in ("claude", "all"):
        skills_dir = generate_skills(repo_root)
        print(f"Generated Claude Code skills in {skills_dir}")

    # Inject instructions
    if target in ("claude", "all"):
        inject_claude_md(repo_root)
    inject_platform_instructions(repo_root, target=target)

    # Install hooks
    if target in ("claude", "all"):
        install_hooks(repo_root, platform="claude")

    print("\nNext steps:")
    print("  1. Restart your AI coding tool to pick up the new config")
    print("  2. Use the conversion tools to convert documents to Markdown!")


def cmd_convert_pdf(args):
    from mcp_document_converter.pdf2markdown_markitdown import pdf_to_markdown_simple
    
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        markdown = pdf_to_markdown_simple(str(file_path))
        
        if args.output:
            Path(args.output).write_text(markdown, encoding="utf-8")
            print(f"Converted successfully: {args.output}")
        else:
            print(markdown)
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_convert_pdf_marker(args):
    from mcp_document_converter.pdf2markdown import convert_pdf_page_by_page
    
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            convert_pdf_page_by_page(str(file_path), tmp_dir)
            output_files = list(Path(tmp_dir).glob("*.md"))
            
            if not output_files:
                print("Error: No output generated", file=sys.stderr)
                sys.exit(1)
            
            combined = [f for f in output_files if "_page_" not in f.name]
            if combined:
                markdown = combined[0].read_text(encoding="utf-8")
            else:
                all_content = []
                for f in sorted(output_files):
                    all_content.append(f.read_text(encoding="utf-8"))
                markdown = "\n\n".join(all_content)
            
            if args.output:
                Path(args.output).write_text(markdown, encoding="utf-8")
                print(f"Converted successfully: {args.output}")
            else:
                print(markdown)
    except ImportError:
        print("Error: marker-pdf not installed. Please install with: pip install doc2md-helper[marker]", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_convert_docx(args):
    from mcp_document_converter.docx2markdown import docx_to_markdown
    
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = docx_to_markdown(str(file_path), tmp_dir)
            markdown = Path(output_path).read_text(encoding="utf-8")
            
            if args.output:
                Path(args.output).write_text(markdown, encoding="utf-8")
                print(f"Converted successfully: {args.output}")
            else:
                print(markdown)
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_convert_excel(args):
    from mcp_document_converter.excel2markdown import excel_to_markdown_simple
    
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        markdown = excel_to_markdown_simple(str(file_path))
        
        if args.output:
            Path(args.output).write_text(markdown, encoding="utf-8")
            print(f"Converted successfully: {args.output}")
        else:
            print(markdown)
    except Exception as e:
        print(f"Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="doc2md-helper",
        description="Document converter for PDF, DOCX, and Excel to Markdown with MCP support",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Show version and exit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Shared platform choices
    platform_choices = [
        "codex", "claude", "claude-code", "cursor", "windsurf", "zed",
        "continue", "opencode", "antigravity", "gemini-cli", "qwen", "kiro",
        "qoder", "copilot", "copilot-cli", "all",
    ]

    # install (primary) + init (alias)
    install_parser = subparsers.add_parser("install", help="Register MCP server with AI coding platforms")
    install_parser.add_argument("--repo", default=None, help="Repository root (auto-detected)")
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    install_parser.add_argument(
        "--platform",
        choices=platform_choices,
        default="all",
        help="Target platform for MCP config (default: all detected)",
    )
    install_parser.set_defaults(func=_handle_init)

    init_parser = subparsers.add_parser("init", help="Alias for install")
    init_parser.add_argument("--repo", default=None, help="Repository root (auto-detected)")
    init_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    init_parser.add_argument(
        "--platform",
        choices=platform_choices,
        default="all",
        help="Target platform for MCP config (default: all detected)",
    )
    init_parser.set_defaults(func=_handle_init)

    # serve / mcp
    serve_parser = subparsers.add_parser(
        "serve",
        help="Start MCP server (stdio by default, or HTTP on localhost with --http)",
    )
    serve_parser.add_argument("--repo", default=None, help="Repository root (auto-detected)")
    serve_parser.add_argument(
        "--http",
        action="store_true",
        help="Listen for MCP over Streamable HTTP on localhost (default port 5555)",
    )
    serve_parser.add_argument(
        "--host",
        default=None,
        metavar="ADDR",
        help="Bind address for --http (default: 127.0.0.1)",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=None,
        metavar="PORT",
        help="Port for --http (default: 5555)",
    )

    mcp_parser = subparsers.add_parser("mcp", help="Alias for serve")
    mcp_parser.add_argument("--repo", default=None, help="Repository root (auto-detected)")

    # convert commands
    convert_pdf_parser = subparsers.add_parser("convert-pdf", help="Convert PDF to Markdown (MarkItDown - fast)")
    convert_pdf_parser.add_argument("file_path", help="Path to PDF file")
    convert_pdf_parser.add_argument("-o", "--output", help="Output file path (optional)")
    convert_pdf_parser.set_defaults(func=cmd_convert_pdf)

    convert_pdf_marker_parser = subparsers.add_parser("convert-pdf-marker", help="Convert PDF to Markdown (Marker - high quality)")
    convert_pdf_marker_parser.add_argument("file_path", help="Path to PDF file")
    convert_pdf_marker_parser.add_argument("-o", "--output", help="Output file path (optional)")
    convert_pdf_marker_parser.set_defaults(func=cmd_convert_pdf_marker)

    convert_docx_parser = subparsers.add_parser("convert-docx", help="Convert Word document to Markdown")
    convert_docx_parser.add_argument("file_path", help="Path to Word file")
    convert_docx_parser.add_argument("-o", "--output", help="Output file path (optional)")
    convert_docx_parser.set_defaults(func=cmd_convert_docx)

    convert_excel_parser = subparsers.add_parser("convert-excel", help="Convert Excel to Markdown")
    convert_excel_parser.add_argument("file_path", help="Path to Excel file")
    convert_excel_parser.add_argument("-o", "--output", help="Output file path (optional)")
    convert_excel_parser.set_defaults(func=cmd_convert_excel)

    args = parser.parse_args()

    if args.version:
        print(f"doc2md-helper {_get_version()}")
        return

    if args.command is None:
        _print_banner()
        return

    if args.command in ("serve", "mcp"):
        from mcp_document_converter.server import main as serve_main

        repo_root = args.repo
        if args.command == "serve":
            transport = "streamable-http" if args.http else "stdio"
            host = args.host
            port = args.port
            serve_main(repo_root=repo_root, transport=transport, host=host, port=port)
        else:
            serve_main(repo_root=repo_root)
        return

    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
