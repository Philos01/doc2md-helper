# Quick Start Guide - doc2md-helper

## 📦 Installation

### Windows Users (Simplest)

1. Install the package:
```bash
pip install doc2md-helper
```

2. Configure for Claude Code:
```bash
doc2md-helper install
```

3. Restart Claude Code - that's it!

### All Platforms

```bash
# 1. Install
pip install doc2md-helper

# 2. Configure your platform
doc2md-helper install --platform claude  # or cursor, codex, etc.

# 3. Restart your AI coding tool
```

---

## 🎯 Quick Usage

### In Claude Code

Just ask naturally:

```
Read this report.pdf
```

You'll be asked which PDF conversion method to use:
1. **MarkItDown** - Fast for text-based PDFs
2. **Marker** - High-precision OCR for scanned PDFs

### Command Line

```bash
# Convert PDF
doc2md-helper convert-pdf document.pdf

# Convert Word
doc2md-helper convert-docx report.docx

# Convert Excel
doc2md-helper convert-excel data.xlsx

# Save to specific file
doc2md-helper convert-pdf document.pdf -o output.md
```

---

## 📁 Project Structure

```
mcp-document-converter/
├── mcp_document_converter/
│   ├── __init__.py
│   ├── cli.py           # CLI commands
│   ├── server.py        # MCP server
│   ├── skills.py        # Platform configs
│   ├── pdf2markdown.py
│   ├── pdf2markdown_markitdown.py
│   ├── docx2markdown.py
│   └── excel2markdown.py
├── demo/                # Example documents
├── pyproject.toml       # Project config
└── README.md            # Full documentation
```

---

## 🔧 Troubleshooting

### If install fails

```bash
# Just install basic version (works great for most PDFs)
pip install doc2md-helper
```

### If platform config not detected

```bash
# Specify platform explicitly
doc2md-helper install --platform claude
```

See full README for more detailed documentation.
