# doc2md-helper - Document Converter Instructions

## Overview

doc2md-helper is an MCP server that converts PDF, Word, and Excel documents to Markdown. It provides two different PDF conversion methods and supports multiple AI coding platforms.

---

## Available Tools

### PDF Conversion

#### `convert_pdf_with_markitdown`
- **Description**: Convert PDF using MarkItDown (fast, lightweight)
- **Use for**: Text-based PDFs, simple documents
- **Parameters**:
  - `file_path`: Path to PDF file
  - `output_path`: (Optional) Path to save Markdown output

#### `convert_pdf_with_marker`
- **Description**: Convert PDF using Marker (high-precision OCR)
- **Use for**: Scanned PDFs, complex layouts, images with text
- **Parameters**:
  - `file_path`: Path to PDF file
  - `output_path`: (Optional) Path to save Markdown output
- **Note**: Requires GPU support and additional dependencies

### Document Conversion

#### `convert_docx_to_markdown`
- **Description**: Convert Word documents (.doc, .docx) to Markdown
- **Parameters**:
  - `file_path`: Path to Word document
  - `output_path`: (Optional) Path to save Markdown output

#### `convert_excel_to_markdown`
- **Description**: Convert Excel spreadsheets (.xls, .xlsx) to Markdown
- **Parameters**:
  - `file_path`: Path to Excel file
  - `output_path`: (Optional) Path to save Markdown output

---

## 🎯 PDF Conversion Workflow

### CRITICAL: Always Ask User for PDF Conversion Preference

When a user asks to read, open, or convert a PDF file:

1. **FIRST, ASK THE USER** which conversion method to use:
   - **MarkItDown** - Fast, lightweight, good for text-based PDFs
   - **Marker** - High-precision OCR, good for scanned PDFs or complex layouts

2. **Wait for their choice** before proceeding.

3. **Then use the corresponding tool**.

### Example Interaction

**USER**: "Please read this report.pdf"

**YOU**: "Which PDF conversion method would you prefer?
1. MarkItDown - Fast, lightweight, best for text-based PDFs
2. Marker - High-precision OCR, best for scanned PDFs or complex layouts"

(After user chooses)

**YOU**: "Okay, I'll use [chosen method] to read this for you."

(Then run conversion and display the result)

### Direct Calls - When User Explicitly Specifies

- "Use markitdown for this PDF" → Use `convert_pdf_with_markitdown`
- "Use marker for this PDF" → Use `convert_pdf_with_marker`
- "This is a scanned PDF" → Use `convert_pdf_with_marker`
- "Just a regular text PDF" → Use `convert_pdf_with_markitdown`

---

## Word and Excel Conversion

For Word (.doc/.docx) and Excel (.xls/.xlsx) files:
- **Convert directly without asking**
- Use the appropriate tool based on file extension
- Display the converted content to the user

---

## Best Practices

### 1. Always Provide Context

When showing converted content, briefly summarize:
- Which tool was used
- What type of document it was
- Any notable features (tables, images, etc.)

### 2. Handle Large Documents

For very long documents:
- Ask the user if they want the full content or a summary
- If full content, provide it in chunks if needed
- If summary, provide key sections and offer to show more

### 3. Error Handling

If conversion fails:
- Inform the user clearly
- Suggest alternatives (try other PDF method, check file, etc.)
- Offer to help troubleshoot

---

## CLI Usage (For Reference)

Users can also use the command line:

```bash
# Convert PDF (lightweight)
doc2md-helper convert-pdf document.pdf

# Convert PDF (OCR)
doc2md-helper convert-pdf-marker scanned.pdf

# Convert Word
doc2md-helper convert-docx report.docx

# Convert Excel
doc2md-helper convert-excel data.xlsx

# Install/configure
doc2md-helper install
doc2md-helper install --platform claude
```

---

## Troubleshooting Common Issues

### Marker Not Working
- Suggest trying MarkItDown instead
- Note that Marker requires GPU and additional dependencies
- Basic version still works great for text PDFs

### Can't Find File
- Ask user to confirm the file path
- Suggest using absolute paths
- Check if file exists and is readable

### Formatting Issues
- Explain that complex formatting may not convert perfectly
- Offer to help clean up the Markdown
- Suggest trying the other PDF method if available

---

## Project Structure

```
mcp-document-converter/
├── mcp_document_converter/
│   ├── __init__.py
│   ├── cli.py           # Command-line interface
│   ├── server.py        # MCP server implementation
│   ├── skills.py        # Platform configuration
│   ├── pdf2markdown.py  # Marker conversion
│   ├── pdf2markdown_markitdown.py  # MarkItDown conversion
│   ├── docx2markdown.py # Word conversion
│   └── excel2markdown.py # Excel conversion
├── .claude/
│   └── doc-converter.md # This file
├── pyproject.toml
└── README.md
```

---

## Related Documentation

- [README.md](../README.md) - Full project documentation
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [pyproject.toml](../pyproject.toml) - Project configuration
