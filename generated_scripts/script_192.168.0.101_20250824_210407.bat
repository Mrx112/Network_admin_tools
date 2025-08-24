@echo off
REM Auto-generated batch script
REM Created: 2025-08-24T21:04:07.443886
REM Target: 192.168.0.101
REM Purpose: 

echo Running script on %COMPUTERNAME%
echo IP Address: 192.168.0.101
echo Script purpose: 
echo Script execution started at %DATE% %TIME%

Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Restart-Service -Force

if %ERRORLEVEL% NEQ 0 (
    echo Script execution failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo Script execution completed successfully at %DATE% %TIME%
pause