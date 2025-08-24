@echo off
REM Auto-generated batch script
REM Created: {timestamp}
REM Target: {target_ip}
REM Purpose: {purpose}

echo Running script on %COMPUTERNAME%
echo IP Address: {target_ip}
echo Script purpose: {purpose}
echo Script execution started at %DATE% %TIME%

{commands}

if %ERRORLEVEL% NEQ 0 (
    echo Script execution failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo Script execution completed successfully at %DATE% %TIME%
pause