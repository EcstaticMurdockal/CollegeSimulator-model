@echo off
echo ============================================================
echo Stopping old server and starting enhanced version...
echo ============================================================
echo.

REM Kill any Python processes running on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Stopping process %%a on port 8000...
    taskkill /F /PID %%a 2>nul
)

timeout /t 2 /nobreak >nul

echo.
echo Starting enhanced College Admissions Simulator...
echo.
echo Features:
echo   - 53 Top US Universities
echo   - 11 Gender Options
echo   - 38 AP Subjects
echo   - Application Rounds (ED/EA/REA/RD)
echo.
echo Server starting on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ============================================================
echo.

cd /d "%~dp0"
python main.py
