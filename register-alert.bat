@echo off
REM
REM register-alert.bat - repository-root wrapper for the AutoAlertStaleRun
REM schtasks registration. One-line forward into step7b so callers from the
REM repo root (double-click, PowerShell alias, whatever) can run:
REM   register-alert.bat        (register / re-register)
REM   register-alert.bat --help (show usage, no schtasks invocation)
REM
REM The actual logic lives in scripts\check\step7b__register_alert_schtasks.bat.
REM

pushd "%~dp0"
call scripts\check\step7b__register_alert_schtasks.bat %*
set "EC=%ERRORLEVEL%"
popd
exit /b %EC%
