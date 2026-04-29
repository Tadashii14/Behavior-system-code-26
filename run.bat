@echo off
REM Canonical trees: ..\v1 (Version 1) and ..\v2 (Version 2). This forwards to v1.
call "%~dp0..\v1\run.bat"
exit /b %ERRORLEVEL%
