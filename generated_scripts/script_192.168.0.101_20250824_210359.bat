@echo off
REM Auto-generated batch script
REM Created: 2025-08-24T21:03:59.499531
REM Target: 192.168.0.101
REM Purpose: Restart Service

echo Running script on %COMPUTERNAME%
echo IP Address: 192.168.0.101
echo Script purpose: Restart Service
echo Script execution started at %DATE% %TIME%

Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Restart-Service -Force

if %ERRORLEVEL% NEQ 0 (
    echo Script execution failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo Script execution completed successfully at %DATE% %TIME%
pause