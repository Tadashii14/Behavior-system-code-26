@echo off
REM ZIMON — single supported runtime: Python 3.10 + PySpin (FLIR). No venv fallbacks.

cd /d "%~dp0"

echo Starting ZIMON...
echo.

where py >nul 2>&1
if not %ERRORLEVEL% equ 0 (
    echo ERROR: The Python launcher ^(py^) was not found.
    echo Install Python 3.10 from https://www.python.org/downloads/
    pause
    exit /b 1
)

py -3.10 -c "import sys; assert sys.version_info[:2] == (3, 10), 'Need Python 3.10'; import PySpin" 2>nul
if not %ERRORLEVEL% equ 0 (
    echo ERROR: Python 3.10 with PySpin is required.
    echo Install Spinnaker SDK and the matching PySpin wheel ^(cp310^), then run again.
    pause
    exit /b 1
)

py -3.10 main.py
exit /b %ERRORLEVEL%
