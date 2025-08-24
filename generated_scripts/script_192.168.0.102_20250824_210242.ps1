# Auto-generated PowerShell script
# Created: 2025-08-24T21:02:42.041879
# Target: 192.168.0.102
# Purpose: Restart Service

Write-Host "Running script on $env:COMPUTERNAME"
Write-Host "IP Address: 192.168.0.102"
Write-Host "Script purpose: Restart Service"
Write-Host "Script execution started at $(Get-Date)"

try {
    # Script commands
    Write-Host 'Executing: Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Restart-Service -Force'
try { Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Restart-Service -Force }
catch { Write-Error $_.Exception.Message }
}
catch {
    Write-Error "Script execution failed: $($_.Exception.Message)"
    exit 1
}

Write-Host "Script execution completed successfully at $(Get-Date)"
Read-Host "Press Enter to continue"