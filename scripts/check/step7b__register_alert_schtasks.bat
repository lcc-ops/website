@echo off
setlocal

REM
REM step7b__register_alert_schtasks.bat - register the AutoAlertStaleRun
REM scheduled task that drives scripts\auto\_alert_stale_run.ps1 daily at
REM 11:00. Mirrors step7a__register_schtasks.bat (which registers the
REM 09:00 daily-batch task) and is intended to be run the same way:
REM   - non-elevated cmd.exe
REM   - same user-context as AutoDailyBlogDraft
REM
REM This bat is a thin wrapper around `schtasks /create`. It is destructive
REM across re-invocations (it deletes any prior task with the same name).
REM Run only when you intend to (re-)register the alarm.
REM

if /I "%~1"=="--help" goto :show_help
if /I "%~1"=="/?" goto :show_help
if /I "%~1"=="-h" goto :show_help

set REPO=D:\LocalSystem\Code\ai_dev\website
set RUNNER=%REPO%\scripts\auto\_alert_stale_run.ps1

if not exist "%RUNNER%" (
    echo FAILED: %RUNNER% not found.
    exit /b 1
)

schtasks /delete /tn "AutoAlertStaleRun" /f >nul 2>&1

REM Register daily 11:00 trigger in the current user's context.
REM 11:00 sits two hours past the 09:00 batch (see step7a) so a successful
REM run that exits 0 still has time to update state.json.last_successful_run_at
REM before the alert's 36 h threshold fires.
REM /ru %USERNAME% is required so PATH and %USERPROFILE%\.claude\ match the
REM same user-context that AutoDailyBlogDraft runs under.
REM /rl highest for the same reason - the alert can write to the LOG path
REM under %USERPROFILE% if you ever pass -LogPath.
schtasks /create ^
  /tn "AutoAlertStaleRun" ^
  /tr "powershell -NoProfile -ExecutionPolicy Bypass -File \"%RUNNER%\"" ^
  /sc daily ^
  /st 11:00:00 ^
  /delay 0001:00 ^
  /rl highest ^
  /ru "%USERNAME%"

if errorlevel 1 (
    echo FAILED to register. Run as Administrator? Or check schtasks syntax.
    exit /b 1
)

echo.
echo Registered. Trigger: schtasks /run /tn AutoAlertStaleRun
echo Inspect:  schtasks /query /tn AutoAlertStaleRun /v /fo LIST
echo Uninstall: schtasks /delete /tn AutoAlertStaleRun /f
endlocal
exit /b 0

:show_help
echo Registers the AutoAlertStaleRun scheduled task (daily 11:00, user-context).
echo Re-runs are destructive (any prior task with the same name is deleted).
echo.
echo Usage:
echo   scripts\check\step7b__register_alert_schtasks.bat
echo.
echo Inspect after running:
echo   schtasks /query /tn AutoAlertStaleRun /v /fo LIST
echo.
echo Uninstall:
echo   schtasks /delete /tn AutoAlertStaleRun /f
endlocal
exit /b 0
