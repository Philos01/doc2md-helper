# 条件导入 marker 版本（可选依赖）
try:
    from mcp_document_converter.pdf2markdown import convert_pdf_page_by_page
    _has_marker = True
except ImportError:
    convert_pdf_page_by_page = None
    _has_marker = False

# 无条件导入其他模块
from mcp_document_converter.pdf2markdown_markitdown import (
    pdf_to_markdown_markitdown,
    pdf_to_markdown_simple,
)
from mcp_document_converter.docx2markdown import docx_to_markdown
from mcp_document_converter.excel2markdown import (
    excel_to_markdown,
    excel_to_markdown_simple,
)

# 构建 __all__
__all__ = [
    "pdf_to_markdown_markitdown",
    "pdf_to_markdown_simple",
    "docx_to_markdown",
    "excel_to_markdown",
    "excel_to_markdown_simple",
]
if _has_marker:
    __all__.append("convert_pdf_page_by_page")
