---
name: Convert Documents
description: Convert PDF, DOCX, and Excel files to Markdown
---

## Convert Documents

Use the doc2md-helper MCP tools to convert documents to Markdown.

### Available Tools

1. **convert_pdf_with_markitdown**: Convert PDFs using MarkItDown (fast, lightweight)
2. **convert_pdf_with_marker**: Convert PDFs using Marker (high-quality OCR)
3. **convert_docx_to_markdown**: Convert Word documents (.docx, .doc)
4. **convert_excel_to_markdown**: Convert Excel spreadsheets (.xlsx, .xls)

### Usage Guide

For PDF conversion:
- Use MarkItDown version for text-based PDFs (faster, no GPU needed)
- Use Marker version for scanned PDFs or complex layouts (better OCR)

All tools automatically save the converted Markdown alongside the original file.

### Tips

- Always specify full file paths for best results
- Output will be saved to the same directory with .md extension
- You can specify a custom output path if needed

