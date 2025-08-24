# Auto-generated PowerShell script
# Created: 2025-08-24T21:04:10.443977
# Target: 192.168.0.101
# Purpose: System Information

Write-Host "Running script on $env:COMPUTERNAME"
Write-Host "IP Address: 192.168.0.101"
Write-Host "Script purpose: System Information"
Write-Host "Script execution started at $(Get-Date)"

try {
    # Script commands
    Write-Host 'Executing: systeminfo'
try { systeminfo }
catch { Write-Error $_.Exception.Message }
Write-Host 'Executing: Get-WmiObject -Class Win32_ComputerSystem | Select-Object Name, Manufacturer, Model'
try { Get-WmiObject -Class Win32_ComputerSystem | Select-Object Name, Manufacturer, Model }
catch { Write-Error $_.Exception.Message }
Write-Host 'Executing: Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption, Version'
try { Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption, Version }
catch { Write-Error $_.Exception.Message }
Write-Host 'Executing: ipconfig /all'
try { ipconfig /all }
catch { Write-Error $_.Exception.Message }
}
catch {
    Write-Error "Script execution failed: $($_.Exception.Message)"
    exit 1
}

Write-Host "Script execution completed successfully at $(Get-Date)"
Read-Host "Press Enter to continue"