@echo off
REM Thin CMD wrapper so schtasks /create can target a .bat file.
setlocal
cd /d "%~dp0\..\.."
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\auto\run_daily_batch.ps1 %*
exit /b %ERRORLEVEL%
