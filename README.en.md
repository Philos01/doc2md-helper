# doc2md-helper

<p align="center">
  <strong>Document Conversion MCP Server</strong>
</p>

<p align="center">
  🇺🇸 English | <a href="README.md">🇨🇳 中文</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/doc2md-helper/"><img src="https://img.shields.io/pypi/v/doc2md-helper?style=flat-square&color=blue" alt="PyPI"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="MIT Licence"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square" alt="Python 3.10+"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-compatible-green.svg?style=flat-square" alt="MCP"></a>
</p>

Convert PDF, Word, and Excel documents to Markdown with full MCP integration and CLI support. Seamlessly works with Claude Code, Cursor, CodeX, and more.

---

## Quick Start

### Installation

```bash
pip install doc2md-helper
doc2md-helper install
```

Then restart your AI coding tool.

### Usage with Claude Code

Just ask naturally:

```
Read this report.pdf file
```

Claude Code will ask which PDF conversion method you prefer:
1. **MarkItDown** - Fast, lightweight, perfect for text-based PDFs
2. **Marker** - High-precision OCR, great for scanned or complex layouts (requires GPU)

### CLI Usage

```bash
# Convert PDF (lightweight)
doc2md-helper convert-pdf document.pdf

# Convert PDF (high-precision OCR)
doc2md-helper convert-pdf-marker scanned.pdf

# Convert Word
doc2md-helper convert-docx report.docx

# Convert Excel
doc2md-helper convert-excel data.xlsx

# Save to specific path
doc2md-helper convert-pdf document.pdf -o output.md
```

---

## Features

- **Multiple PDF Conversion Options**: Choose between lightweight MarkItDown or high-precision Marker
- **Full MCP Integration**: Works with Claude Code, Cursor, CodeX, Windsurf, Zed, and more
- **CLI Interface**: Convert documents directly from the command line
- **Multi-Format Support**: PDF, DOCX, DOC, XLSX, XLS
- **Automatic Platform Detection**: Install configures all supported platforms automatically

---

## Installation

### Basic Installation

```bash
pip install doc2md-helper
```

This installs core dependencies: `mcp`, `markitdown[pdf]`, `openpyxl`, `python-docx`, `mammoth`.

### With Marker Support (High-Precision OCR)

```bash
pip install doc2md-helper[marker]
```

Requires additional dependencies: `marker-pdf`, `torch`, `bitsandbytes`, `PyPDF2`.

### Full Installation

```bash
pip install doc2md-helper[all]
```

Includes marker support plus additional optional dependencies.

### Install from Source

```bash
git clone https://github.com/Philos01/doc2md-helper
cd doc2md-helper
pip install -e .
```

---

## Platform Setup

### Claude Code

```bash
doc2md-helper install --platform claude
```

Configures `~/.claude/settings.json`. Restart Claude Code after installation.

### Cursor

```bash
doc2md-helper install --platform cursor
```

Configures `.cursor/mcp.json` in your project directory.

### Other Platforms

```bash
doc2md-helper install --platform <platform-name>
```

Supported platforms: `claude`, `cursor`, `codex`, `windsurf`, `zed`, `continue`, `opencode`, `gemini-cli`, `qwen`, `kiro`, `qoder`, `copilot`, `copilot-cli`, or `all`.

### Manual Configuration

If auto-configuration fails, add manually to your platform's MCP config:

```json
{
  "mcpServers": {
    "doc2md-helper": {
      "command": "doc2md-helper",
      "args": ["serve"]
    }
  }
}
```

---

## Usage

### MCP Tools

| Tool | Description |
|------|-------------|
| `convert_pdf_with_markitdown` | Convert PDF using MarkItDown (fast, lightweight) |
| `convert_pdf_with_marker` | Convert PDF using Marker (high-precision OCR) |
| `convert_docx_to_markdown` | Convert Word documents |
| `convert_excel_to_markdown` | Convert Excel spreadsheets |

### CLI Commands

```bash
# Document conversion
doc2md-helper convert-pdf <file>
doc2md-helper convert-pdf-marker <file>
doc2md-helper convert-docx <file>
doc2md-helper convert-excel <file>

# Installation and setup
doc2md-helper install
doc2md-helper install --platform <name>

# MCP server
doc2md-helper serve
doc2md-helper serve --http --host 127.0.0.1 --port 5555
```

---

## PDF Conversion Options

| Method | Description | Best For | Dependencies |
|--------|-------------|----------|-------------|
| **MarkItDown** | Fast, lightweight | Text-based PDFs | markitdown |
| **Marker** | High-precision OCR | Scanned PDFs, complex layouts | marker-pdf, torch |

---

## Project Structure

```
doc2md-helper/
├── mcp_document_converter/
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── server.py              # MCP server implementation
│   ├── skills.py              # Platform configuration and skills
│   ├── pdf2markdown.py        # Marker PDF conversion
│   ├── pdf2markdown_markitdown.py  # MarkItDown PDF conversion
│   ├── docx2markdown.py       # Word document conversion
│   └── excel2markdown.py      # Excel spreadsheet conversion
├── .claude/
│   └── doc-converter.md       # Claude Code instructions
├── demo/                      # Example documents
├── pyproject.toml             # Project configuration
└── README.md                  # Chinese documentation (default)
```

---

## Development

### Setup Development Environment

```bash
git clone https://github.com/Philos01/doc2md-helper
cd doc2md-helper
pip install -e ".[dev]"
```

### Running Tests

```bash
# Add tests here
```

---

## Troubleshooting

### Installation Issues

If you encounter problems with `marker-pdf`:

```bash
pip install doc2md-helper  # Just install the basic version
```

The basic version works great for text-based PDFs.

### Platform Configuration Not Working

Try specifying the platform explicitly:

```bash
doc2md-helper install --platform claude
```

Or configure manually as shown in the "Manual Configuration" section.

---

## Contributing

Contributions welcome! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Related Projects

- [code-review-graph](https://github.com/tirth8205/code-review-graph) - Code understanding with knowledge graphs (the inspiration for this project's architecture)
