# doc2md-helper

<p align="center">
  <strong>文档转换 MCP 服务器</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/doc2md-helper/"><img src="https://img.shields.io/pypi/v/doc2md-helper?style=flat-square&color=blue" alt="PyPI"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="MIT Licence"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square" alt="Python 3.10+"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-compatible-green.svg?style=flat-square" alt="MCP"></a>
</p>

将 PDF、Word 和 Excel 文档转换为 Markdown，支持完整的 MCP 集成和 CLI 功能。无缝适配 Claude Code、Cursor、CodeX 等平台。

---

## 快速开始

### 安装

```bash
pip install doc2md-helper
doc2md-helper install
```

然后重启你的 AI 编码工具。

### 在 Claude Code 中使用

直接自然语言提问：

```
读取这个 report.pdf 文件
```

Claude Code 会询问你偏好哪种 PDF 转换方式：
1. **MarkItDown** - 快速、轻量，完美适合文本型 PDF
2. **Marker** - 高精度 OCR，适合扫描版或复杂排版（需要 GPU）

### 命令行使用

```bash
# 转换 PDF（轻量版）
doc2md-helper convert-pdf document.pdf

# 转换 PDF（高精度 OCR 版）
doc2md-helper convert-pdf-marker scanned.pdf

# 转换 Word
doc2md-helper convert-docx report.docx

# 转换 Excel
doc2md-helper convert-excel data.xlsx

# 保存到指定路径
doc2md-helper convert-pdf document.pdf -o output.md
```

---

## 功能特性

- **多种 PDF 转换选项**：在轻量的 MarkItDown 和高精度的 Marker 之间选择
- **完整 MCP 集成**：支持 Claude Code、Cursor、CodeX、Windsurf、Zed 等平台
- **命令行界面**：直接从命令行转换文档
- **多格式支持**：PDF、DOCX、DOC、XLSX、XLS
- **自动平台检测**：安装时自动配置所有支持的平台

---

## 安装

### 基础安装

```bash
pip install doc2md-helper
```

这会安装核心依赖：`mcp`、`markitdown[pdf]`、`openpyxl`、`python-docx`、`mammoth`。

### 带 Marker 支持（高精度 OCR）

```bash
pip install doc2md-helper[marker]
```

需要额外依赖：`marker-pdf`、`torch`、`bitsandbytes`、`PyPDF2`。

### 完整安装

```bash
pip install doc2md-helper[all]
```

包含 marker 支持以及额外的可选依赖。

### 从源码安装

```bash
git clone https://github.com/your-username/mcp-document-converter
cd mcp-document-converter
pip install -e .
```

---

## 平台配置

### Claude Code

```bash
doc2md-helper install --platform claude
```

配置 `~/.claude/settings.json`。安装后重启 Claude Code。

### Cursor

```bash
doc2md-helper install --platform cursor
```

在项目目录中配置 `.cursor/mcp.json`。

### 其他平台

```bash
doc2md-helper install --platform <平台名称>
```

支持的平台：`claude`、`cursor`、`codex`、`windsurf`、`zed`、`continue`、`opencode`、`gemini-cli`、`qwen`、`kiro`、`qoder`、`copilot`、`copilot-cli`，或 `all`。

### 手动配置

如果自动配置失败，手动添加到你平台的 MCP 配置中：

```json
{
  "mcpServers": {
    "doc2md-helper": {
      "command": "uvx",
      "args": ["doc2md-helper", "serve"]
    }
  }
}
```

---

## 使用方法

### MCP 工具

| 工具 | 描述 |
|------|------|
| `convert_pdf_with_markitdown` | 使用 MarkItDown 转换 PDF（快速、轻量） |
| `convert_pdf_with_marker` | 使用 Marker 转换 PDF（高精度 OCR） |
| `convert_docx_to_markdown` | 转换 Word 文档 |
| `convert_excel_to_markdown` | 转换 Excel 电子表格 |

### CLI 命令

```bash
# 文档转换
doc2md-helper convert-pdf <文件>
doc2md-helper convert-pdf-marker <文件>
doc2md-helper convert-docx <文件>
doc2md-helper convert-excel <文件>

# 安装和设置
doc2md-helper install
doc2md-helper install --platform <名称>

# MCP 服务器
doc2md-helper serve
doc2md-helper serve --http --host 127.0.0.1 --port 5555
```

---

## PDF 转换选项

| 方式 | 描述 | 最适合 | 依赖 |
|------|------|--------|------|
| **MarkItDown** | 快速、轻量 | 文本型 PDF | markitdown |
| **Marker** | 高精度 OCR | 扫描版 PDF、复杂排版 | marker-pdf, torch |

---

## 项目结构

```
mcp-document-converter/
├── mcp_document_converter/
│   ├── __init__.py
│   ├── cli.py                 # 命令行界面
│   ├── server.py              # MCP 服务器实现
│   ├── skills.py              # 平台配置和技能
│   ├── pdf2markdown.py        # Marker PDF 转换
│   ├── pdf2markdown_markitdown.py  # MarkItDown PDF 转换
│   ├── docx2markdown.py       # Word 文档转换
│   └── excel2markdown.py      # Excel 电子表格转换
├── .claude/
│   └── doc-converter.md       # Claude Code 指令
├── demo/                      # 示例文档
├── pyproject.toml             # 项目配置
└── README.md                  # 本文件
```

---

## 开发

### 搭建开发环境

```bash
git clone https://github.com/your-username/mcp-document-converter
cd mcp-document-converter
pip install -e ".[dev]"
```

### 运行测试

```bash
# 在此添加测试
```

---

## 故障排除

### 安装问题

如果遇到 `marker-pdf` 相关问题：

```bash
pip install doc2md-helper  # 只需安装基础版本
```

基础版本对文本型 PDF 效果很好。

### 平台配置不工作

尝试显式指定平台：

```bash
doc2md-helper install --platform claude
```

或按照"手动配置"部分说明手动配置。

---

## 贡献

欢迎贡献！请随时：
- 报告 bug
- 提出功能建议
- 提交 pull request

---

## 许可证

MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

---

## 相关项目

- [code-review-graph](https://github.com/tirth8205/code-review-graph) - 使用知识图谱理解代码（本项目架构的灵感来源）
