@echo off
git add .
if %errorlevel% neq 0 (
    echo Failed to add files
    pause
    exit /b 1
)
set /p msg="Enter Commit Message: "
git commit -m "%msg%"
if %errorlevel% neq 0 (
    echo Failed to commit
    pause
    exit /b 1
)
git push origin main
if %errorlevel% neq 0 (
    echo Failed to push
    pause
    exit /b 1
)
echo Success
pause