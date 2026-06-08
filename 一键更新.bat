@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   影视源一键更新
echo ========================================
echo.

:: 检查 git 是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Git，请先安装 Git
    pause
    exit /b 1
)

:: 检查是否有变更
for /f %%i in ('git status --porcelain') do set "HAS_CHANGES=1"
if not defined HAS_CHANGES (
    echo [INFO] 没有文件变更，无需提交
    pause
    exit /b 0
)

:: 显示变更文件
echo [INFO] 检测到以下变更：
git status --short
echo.

:: 自动添加所有变更
git add .
echo.

:: 读取上次 commit 消息用于提示
for /f "delims=" %%m in ('git log -1 --format="%%s" 2^>nul') do set "LAST_MSG=%%m"

:: 使用日期时间作为 commit 消息
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set "TODAY=%%a%%b%%c"
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set "NOW=%%a%%b"
set "COMMIT_MSG=更新影视源 %date% %time%"

echo ----------------------------------------
echo 即将提交并推送：
echo   %COMMIT_MSG%
echo ----------------------------------------
echo.
set /p CONFIRM=确认推送？(Y/N):
if /i not "%CONFIRM%"=="Y" (
    echo 已取消
    git reset HEAD >nul 2>&1
    pause
    exit /b 0
)

:: 提交
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [错误] 提交失败
    pause
    exit /b 1
)

:: 推送
echo.
echo [INFO] 正在推送到 GitHub...
git push
if errorlevel 1 (
    echo [错误] 推送失败，可能需要先 git pull
    pause
    exit /b 1
)

echo.
echo ========================================
echo   推送成功！
echo ========================================
echo.
echo GitHub Pages 约需 1~3 分钟同步更新
echo 配置地址：https://wwh3602.github.io/tvbox-source/config.json
echo.
pause
