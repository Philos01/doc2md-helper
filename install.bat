
@echo off
echo ================================================
echo   Doc2MD Helper - 一键安装脚本
echo ================================================
echo.

echo [1/3] 安装 Python 包...
pip install -e .
if errorlevel 1 (
    echo 安装失败！
    pause
    exit /b 1
)
echo.

echo [2/3] 配置 Claude Code...
doc2md-helper install --platform claude-code
echo.

echo [3/3] 完成！
echo ================================================
echo.
echo 安装已完成！请重启 Claude Code 即可使用。
echo.
echo 可用命令：
echo   doc2md-helper convert-pdf    ^<文件路径^>
echo   doc2md-helper convert-docx   ^<文件路径^>
echo   doc2md-helper convert-excel  ^<文件路径^>
echo.
pause
