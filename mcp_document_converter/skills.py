"""Doc2Md Helper skills and hooks auto-install.

Generates Claude Code agent skill files, hooks configuration, and
CLAUDE.md integration for seamless doc2md-helper usage.
Also supports multi-platform MCP server installation.
"""

from __future__ import annotations

import json
import logging
import os
import platform
import re
import shutil
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# --- Multi-platform MCP install ---

def _zed_settings_path() -> Path:
    """Return the Zed settings.json path for the current OS."""
    if platform.system() == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Zed" / "settings.json"
    return Path.home() / ".config" / "zed" / "settings.json"


PLATFORMS: dict[str, dict[str, Any]] = {
    "codex": {
        "name": "Codex",
        "config_path": lambda root: Path.home() / ".codex" / "config.toml",
        "key": "mcp_servers",
        "detect": lambda: (Path.home() / ".codex").exists(),
        "format": "toml",
        "needs_type": True,
    },
    "claude": {
        "name": "Claude Code",
        "config_path": lambda root: root / ".mcp.json",
        "key": "mcpServers",
        "detect": lambda: True,
        "format": "object",
        "needs_type": True,
    },
    "cursor": {
        "name": "Cursor",
        "config_path": lambda root: root / ".cursor" / "mcp.json",
        "key": "mcpServers",
        "detect": lambda: (Path.home() / ".cursor").exists(),
        "format": "object",
        "needs_type": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "config_path": lambda root: Path.home() / ".codeium" / "windsurf" / "mcp_config.json",
        "key": "mcpServers",
        "detect": lambda: (Path.home() / ".codeium" / "windsurf").exists(),
        "format": "object",
        "needs_type": False,
    },
    "zed": {
        "name": "Zed",
        "config_path": lambda root: _zed_settings_path(),
        "key": "context_servers",
        "detect": lambda: _zed_settings_path().parent.exists(),
        "format": "object",
        "needs_type": False,
    },
    "continue": {
        "name": "Continue",
        "config_path": lambda root: Path.home() / ".continue" / "config.json",
        "key": "mcpServers",
        "detect": lambda: (Path.home() / ".continue").exists(),
        "format": "array",
        "needs_type": True,
    },
    "opencode": {
        "name": "OpenCode",
        "config_path": lambda root: root / ".opencode.json",
        "key": "mcpServers",
        "detect": lambda: True,
        "format": "object",
        "needs_type": True,
    },
    "antigravity": {
        "name": "Antigravity",
        "config_path": lambda root: Path.home() / ".gemini" / "antigravity" / "mcp_config.json",
        "key": "mcpServers",
        "detect": lambda: (Path.home() / ".gemini" / "antigravity").exists(),
        "format": "object",
        "needs_type": False,
    },
    "gemini-cli": {
        "name": "Gemini CLI",
        "config_path": lambda root: root / ".gemini" / "settings.json",
        "key": "mcpServers",
        "detect": lambda: bool(shutil.which("gemini")) or (Path.home() / ".gemini").exists(),
        "format": "object",
        "needs_type": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "config_path": lambda root: Path.home() / ".qwen" / "settings.json",
        "key": "mcpServers",
        "detect": lambda: (Path.home() / ".qwen").exists(),
        "format": "object",
        "needs_type": True,
    },
    "kiro": {
        "name": "Kiro",
        "config_path": lambda root: root / ".kiro" / "settings" / "mcp.json",
        "key": "mcpServers",
        "detect": lambda: (Path.home() / ".kiro").exists(),
        "format": "object",
        "needs_type": True,
    },
    "qoder": {
        "name": "Qoder",
        "config_path": lambda root: root / ".qoder" / "mcp.json",
        "key": "mcpServers",
        "detect": lambda: True,
        "format": "object",
        "needs_type": True,
    },
    "copilot": {
        "name": "GitHub Copilot",
        "config_path": lambda root: root / ".vscode" / "mcp.json",
        "key": "servers",
        "detect": lambda: (Path.home() / ".vscode").exists(),
        "format": "object",
        "needs_type": True,
    },
    "copilot-cli": {
        "name": "GitHub Copilot CLI",
        "config_path": lambda root: Path.home() / ".copilot" / "mcp-config.json",
        "key": "servers",
        "detect": lambda: (Path.home() / ".copilot").exists(),
        "format": "object",
        "needs_type": True,
    },
}


def _in_poetry_project() -> bool:
    """Return True when the running interpreter is a Poetry-managed virtualenv."""
    if os.environ.get("POETRY_ACTIVE") == "1":
        return True
    virtual_env = os.environ.get("VIRTUAL_ENV", "")
    return bool(virtual_env) and "pypoetry" in virtual_env.lower()


def _in_uv_project() -> bool:
    """Return True if `sys.executable` lives inside a uv-managed project."""
    exe = Path(sys.executable).resolve()
    home = Path.home()
    for parent in exe.parents:
        if (parent / "uv.lock").exists():
            return True
        if parent == home or parent == parent.parent:
            break
    return False


def _detect_serve_command() -> tuple[str, list[str]]:
    """Return `(command, args)` that correctly launches `doc2md-helper serve`.

    Priority order:
    1. Direct `doc2md-helper` command (fastest, no virtual env overhead)
    2. Poetry-managed project
    3. uv-managed project
    4. uvx (slow, creates isolated env each time)
    5. Python module fallback
    """
    if shutil.which("doc2md-helper"):
        return ("doc2md-helper", ["serve"])

    if _in_poetry_project():
        poetry = shutil.which("poetry")
        if poetry:
            return ("poetry", ["run", "doc2md-helper", "serve"])

    if os.environ.get("UV_PROJECT_ENVIRONMENT") or _in_uv_project():
        uv = shutil.which("uv")
        if uv:
            return ("uv", ["run", "doc2md-helper", "serve"])

    if shutil.which("uvx"):
        return ("uvx", ["doc2md-helper", "serve"])

    return (sys.executable, ["-m", "mcp_document_converter", "serve"])


def _build_server_entry(
    plat: dict[str, Any], key: str = "", repo_root: "Path | None" = None,
) -> dict[str, Any]:
    """Build the MCP server entry for a platform."""
    command, args = _detect_serve_command()
    entry: dict[str, Any] = {"command": command, "args": args}
    if repo_root is not None:
        entry["cwd"] = str(repo_root)
    if plat["needs_type"]:
        entry["type"] = "stdio"
    if key == "opencode":
        entry["env"] = []
    return entry


def _format_toml_value(value: Any) -> str:
    """Format a primitive Python value as TOML."""
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "[" + ", ".join(_format_toml_value(item) for item in value) + "]"
    raise TypeError(f"Unsupported TOML value: {type(value)!r}")


def _merge_toml_mcp_server(
    config_path: Path,
    server_name: str,
    server_entry: dict[str, Any],
    dry_run: bool = False,
) -> bool:
    """Append a Codex MCP server section without clobbering the rest of the file."""
    section_header = f"[mcp_servers.{server_name}]"
    existing = ""
    if config_path.exists():
        existing = config_path.read_text(encoding="utf-8")
        if section_header in existing:
            return False

    section_lines = [section_header]
    for key, value in server_entry.items():
        section_lines.append(f"{key} = {_format_toml_value(value)}")
    section = "\n".join(section_lines) + "\n"

    if dry_run:
        return True

    config_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = ""
    if existing:
        prefix = existing if existing.endswith("\n") else existing + "\n"
        if not prefix.endswith("\n\n"):
            prefix += "\n"
    config_path.write_text(prefix + section, encoding="utf-8")
    return True


def install_platform_configs(
    repo_root: Path,
    target: str = "all",
    dry_run: bool = False,
) -> list[str]:
    """Install MCP config for one or all detected platforms."""
    if target == "all":
        platforms_to_install = {k: v for k, v in PLATFORMS.items() if v["detect"]()}
        if "kiro" not in platforms_to_install and (repo_root / ".kiro").is_dir():
            platforms_to_install["kiro"] = PLATFORMS["kiro"]
    else:
        if target not in PLATFORMS:
            logger.error("Unknown platform: %s", target)
            return []
        platforms_to_install = {target: PLATFORMS[target]}

    configured: list[str] = []

    for key, plat in platforms_to_install.items():
        config_path: Path = plat["config_path"](repo_root)
        server_key = plat["key"]
        server_entry = _build_server_entry(plat, key=key, repo_root=repo_root)

        if plat["format"] == "toml":
            changed = _merge_toml_mcp_server(
                config_path,
                "doc2md-helper",
                server_entry,
                dry_run=dry_run,
            )
            if not changed:
                print(f"  {plat['name']}: already configured in {config_path}")
                configured.append(plat["name"])
                continue
            if dry_run:
                print(f"  [dry-run] {plat['name']}: would write {config_path}")
            else:
                print(f"  {plat['name']}: configured {config_path}")
            configured.append(plat["name"])
            continue

        existing: dict[str, Any] = {}
        if config_path.exists():
            raw = config_path.read_text(encoding="utf-8", errors="replace")
            stripped = re.sub(r'//.*?$', '', raw, flags=re.MULTILINE)
            stripped = re.sub(r',(\s*[}\]])', r'\1', stripped)
            try:
                existing = json.loads(stripped)
            except (json.JSONDecodeError, OSError):
                print(f"  {plat['name']}: {config_path} contains "
                      f"unparseable JSON — skipping to avoid data loss. "
                      f"Please add the MCP config manually.")
                continue

        if plat["format"] == "array":
            arr = existing.get(server_key, [])
            if not isinstance(arr, list):
                arr = []
            if any(isinstance(s, dict) and s.get("name") == "doc2md-helper" for s in arr):
                print(f"  {plat['name']}: already configured in {config_path}")
                configured.append(plat["name"])
                continue
            arr_entry = {"name": "doc2md-helper", **server_entry}
            arr.append(arr_entry)
            existing[server_key] = arr
        else:
            servers = existing.get(server_key, {})
            if not isinstance(servers, dict):
                servers = {}
            if "doc2md-helper" in servers:
                print(f"  {plat['name']}: already configured in {config_path}")
                configured.append(plat["name"])
                continue
            servers["doc2md-helper"] = server_entry
            existing[server_key] = servers

        if dry_run:
            print(f"  [dry-run] {plat['name']}: would write {config_path}")
        else:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
            print(f"  {plat['name']}: configured {config_path}")

        configured.append(plat["name"])

    return configured


# --- Skill file contents ---

_SKILLS: dict[str, dict[str, str]] = {
    "convert-documents.md": {
        "name": "Convert Documents",
        "description": "Convert PDF, DOCX, and Excel files to Markdown",
        "body": (
            "## Convert Documents\n\n"
            "Use the doc2md-helper MCP tools to convert documents to Markdown.\n\n"
            "### Available Tools\n\n"
            "1. **convert_pdf_with_markitdown**: Convert PDFs using MarkItDown (fast, lightweight)\n"
            "2. **convert_pdf_with_marker**: Convert PDFs using Marker (high-quality OCR)\n"
            "3. **convert_docx_to_markdown**: Convert Word documents (.docx, .doc)\n"
            "4. **convert_excel_to_markdown**: Convert Excel spreadsheets (.xlsx, .xls)\n\n"
            "### Usage Guide\n\n"
            "For PDF conversion:\n"
            "- Use MarkItDown version for text-based PDFs (faster, no GPU needed)\n"
            "- Use Marker version for scanned PDFs or complex layouts (better OCR)\n\n"
            "All tools automatically save the converted Markdown alongside the original file.\n\n"
            "### Tips\n\n"
            "- Always specify full file paths for best results\n"
            "- Output will be saved to the same directory with .md extension\n"
            "- You can specify a custom output path if needed\n"
        ),
    },
}


def generate_skills(repo_root: Path, skills_dir: Path | None = None) -> Path:
    """Generate Claude Code skill files."""
    if skills_dir is None:
        skills_dir = repo_root / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    for filename, skill in _SKILLS.items():
        skill_name = filename.removesuffix(".md")
        skill_subdir = skills_dir / skill_name
        skill_subdir.mkdir(parents=True, exist_ok=True)
        path = skill_subdir / "skill.md"
        content = (
            "---\n"
            f"name: {skill['name']}\n"
            f"description: {skill['description']}\n"
            "---\n\n"
            f"{skill['body']}\n"
        )
        path.write_text(content, encoding="utf-8")
        logger.info("Wrote skill: %s", path)

    return skills_dir


def generate_hooks_config(repo_root: Path) -> dict[str, Any]:
    """Generate Claude Code hooks configuration."""
    return {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "echo 'doc2md-helper ready to convert documents!'",
                            "timeout": 10,
                        },
                    ],
                },
            ],
        }
    }


def install_hooks(repo_root: Path, platform: str = "claude") -> None:
    """Write hooks config to platform-specific settings.json."""
    if platform == "qoder":
        settings_dir = repo_root / ".qoder"
    else:
        settings_dir = repo_root / ".claude"
    settings_dir.mkdir(parents=True, exist_ok=True)
    settings_path = settings_dir / "settings.json"

    existing: dict[str, Any] = {}
    if settings_path.exists():
        try:
            existing = json.loads(settings_path.read_text(encoding="utf-8", errors="replace"))
            backup_path = settings_dir / "settings.json.bak"
            shutil.copy2(settings_path, backup_path)
            logger.info("Backed up existing settings to %s", backup_path)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not read existing %s: %s", settings_path, exc)

    hooks_config = generate_hooks_config(repo_root)
    existing_hooks = existing.get("hooks", {})
    if not isinstance(existing_hooks, dict):
        logger.warning("Existing hooks config is not a dict; replacing with defaults")
        existing_hooks = {}

    merged_hooks = dict(existing_hooks)
    for hook_name, hook_entries in hooks_config.get("hooks", {}).items():
        if isinstance(merged_hooks.get(hook_name), list):
            merged_list = list(merged_hooks[hook_name])
            for entry in hook_entries:
                if entry not in merged_list:
                    merged_list.append(entry)
            merged_hooks[hook_name] = merged_list
        else:
            merged_hooks[hook_name] = hook_entries

    existing["hooks"] = merged_hooks

    settings_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    logger.info("Wrote hooks config: %s", settings_path)


_CLAUDE_MD_SECTION_MARKER = "<!-- doc2md-helper MCP tools -->"

_CLAUDE_MD_SECTION = f"""{_CLAUDE_MD_SECTION_MARKER}
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
"""


# Maps instruction file path → (marker, section) for files that need content
_PLATFORM_INSTRUCTION_CUSTOM_SECTIONS: dict[str, tuple[str, str]] = {
}


def _inject_instructions(file_path: Path, marker: str, section: str) -> bool:
    """Append an instruction section to a file if not already present."""
    existing = ""
    if file_path.exists():
        existing = file_path.read_text(encoding="utf-8", errors="replace")

    if marker in existing:
        logger.info("%s already contains instructions, skipping.", file_path.name)
        return False

    separator = "\n" if existing and not existing.endswith("\n") else ""
    extra_newline = "\n" if existing else ""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(existing + separator + extra_newline + section, encoding="utf-8")
    logger.info("Appended MCP tools section to %s", file_path)
    return True


def inject_claude_md(repo_root: Path) -> None:
    """Append MCP tools section to CLAUDE.md."""
    _inject_instructions(
        repo_root / "CLAUDE.md",
        _CLAUDE_MD_SECTION_MARKER,
        _CLAUDE_MD_SECTION,
    )


# Cross-platform instruction files and which platforms own each one.
_PLATFORM_INSTRUCTION_FILES: dict[str, tuple[str, ...]] = {
    "AGENTS.md": ("cursor", "opencode", "antigravity"),
    "GEMINI.md": ("antigravity", "gemini-cli"),
    ".cursorrules": ("cursor",),
    ".windsurfrules": ("windsurf",),
    "QODER.md": ("qoder",),
    ".kiro/steering/doc2md-helper.md": ("kiro",),
}


def inject_platform_instructions(repo_root: Path, target: str = "all") -> list[str]:
    """Inject 'use converter tools' instructions into platform rule files."""
    updated: list[str] = []
    for filename, owners in _PLATFORM_INSTRUCTION_FILES.items():
        if target != "all" and target not in owners:
            continue
        path = repo_root / filename
        if filename in _PLATFORM_INSTRUCTION_CUSTOM_SECTIONS:
            marker, section = _PLATFORM_INSTRUCTION_CUSTOM_SECTIONS[filename]
        else:
            marker, section = _CLAUDE_MD_SECTION_MARKER, _CLAUDE_MD_SECTION
        if _inject_instructions(path, marker, section):
            updated.append(filename)
    return updated
