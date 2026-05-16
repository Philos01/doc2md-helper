# CLAUDE.md - Project Context for Claude Code

## Project Overview

**doc2md-helper** is an MCP server that converts PDF, Word, and Excel documents to Markdown with two different PDF conversion methods. It provides seamless integration with Claude Code, Cursor, and many other AI coding platforms through FastMCP.

---

## Architecture

- **Core Package**: `mcp_document_converter/` (Python 3.10+)
  - `cli.py` — CLI entry point with `install`, `init`, `serve`, `mcp`, and conversion commands
  - `server.py` — FastMCP server implementation, registers 4 document conversion tools
  - `skills.py` — Platform configuration generation for 15+ AI coding platforms
  - `pdf2markdown.py` — Marker-based high-precision PDF conversion with OCR
  - `pdf2markdown_markitdown.py` — Lightweight MarkItDown PDF conversion
  - `docx2markdown.py` — Word document (.doc, .docx) conversion
  - `excel2markdown.py` — Excel spreadsheet (.xls, .xlsx) conversion
  - `__init__.py` — Package metadata and version

---

## Key Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project configuration, dependencies, entry points |
| `mcp.json` | MCP server configuration template |
| `install.bat` | Windows installation helper script |
| `README.md` | Full project documentation |
| `README.zh-CN.md` | Chinese documentation |
| `QUICKSTART.md` | Quick start guide |
| `.claude/doc-converter.md` | Claude Code specific instructions |

---

## Key Commands

```bash
# Development
pip install -e .          # Install in development mode

# CLI Usage
doc2md-helper --help      # Show all commands
doc2md-helper install     # Auto-configure for all platforms
doc2md-helper install --platform claude  # Configure Claude Code only
doc2md-helper serve       # Start MCP server (stdio)
doc2md-helper serve --http --port 5555  # HTTP server

# Document Conversion
doc2md-helper convert-pdf document.pdf
doc2md-helper convert-pdf-marker scanned.pdf
doc2md-helper convert-docx report.docx
doc2md-helper convert-excel data.xlsx
```

---

## Code Conventions

- **Python target**: 3.10+
- **Line length**: Follow existing style (generally 100-120 chars)
- **FastMCP**: Use `@mcp.tool()` decorator for tool registration
- **Error handling**: Catch specific exceptions, provide user-friendly messages
- **File paths**: Use `Path` from `pathlib` for cross-platform compatibility
- **Windows compatibility**: Use `asyncio.set_event_loop_policy()` on Windows for stdio transport

---

## MCP Tools

The project provides these MCP tools via FastMCP:

| Tool | Purpose |
|------|---------|
| `convert_pdf_with_markitdown` | Lightweight PDF to Markdown (text-based PDFs) |
| `convert_pdf_with_marker` | High-precision OCR PDF conversion (scanned PDFs) |
| `convert_docx_to_markdown` | Word document to Markdown |
| `convert_excel_to_markdown` | Excel spreadsheet to Markdown |

**IMPORTANT**: When converting PDFs, always ask the user which method they prefer first!

---

## Supported Platforms

The `skills.py` module supports configuration for:

- `claude` - Claude Code
- `cursor` - Cursor
- `codex` - CodeX
- `windsurf` - Windsurf
- `zed` - Zed
- `continue` - Continue
- `opencode` - OpenCode
- `gemini-cli` - Gemini CLI
- `qwen` - Qwen
- `kiro` - Kiro
- `qoder` - Qoder
- `copilot` - GitHub Copilot
- `copilot-cli` - GitHub Copilot CLI

---

## Development Workflow

1. Install in development mode: `pip install -e .`
2. Test CLI: `doc2md-helper --help`
3. Test server: `doc2md-helper serve`
4. Make changes to relevant modules
5. Test conversion with sample files in `demo/`

---

## Project Structure

```
mcp-document-converter/
├── mcp_document_converter/
│   ├── __init__.py
│   ├── cli.py                 # CLI commands
│   ├── server.py              # FastMCP server
│   ├── skills.py              # Platform configs
│   ├── pdf2markdown.py        # Marker PDF
│   ├── pdf2markdown_markitdown.py  # MarkItDown PDF
│   ├── docx2markdown.py       # Word conversion
│   └── excel2markdown.py      # Excel conversion
├── .claude/
│   └── doc-converter.md       # Claude instructions
├── demo/                      # Sample documents
├── pyproject.toml             # Project config
├── mcp.json                   # MCP config template
├── install.bat                # Windows installer
├── README.md                  # Full docs
├── README.zh-CN.md            # Chinese docs
└── QUICKSTART.md              # Quick start
```

---

## Related Documentation

- [README.md](README.md) - Complete project documentation
- [.claude/doc-converter.md](.claude/doc-converter.md) - Claude Code specific usage instructions
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [pyproject.toml](pyproject.toml) - Project dependencies and configuration

<!-- doc2md-helper MCP tools -->
## MCP Tools: doc2md-helper

**IMPORTANT: This project has document conversion tools available. Use the
doc2md-helper MCP tools to convert PDF, DOCX, and Excel files to Markdown.**

### Available Tools

| Tool | Use when |
| ------ | ---------- |
| `convert_pdf_with_markitdown` | Convert text-based PDFs quickly |
| `convert_pdf_with_marker` | Convert scanned PDFs with high-quality OCR |
| `convert_docx_to_markdown` | Convert Word documents (.docx, .doc) |
| `convert_excel_to_markdown` | Convert Excel spreadsheets |

### When to Use

- **PDFs**: Try MarkItDown first for text-based PDFs. Use Marker for scanned documents.
- **Word**: Always use `convert_docx_to_markdown`
- **Excel**: Always use `convert_excel_to_markdown`

### Notes

All tools will save the converted Markdown alongside the original file.
