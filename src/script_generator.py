import os
import json
import datetime
from pathlib import Path

class ScriptGenerator:
    def __init__(self):
        self.script_templates = {
            "batch": self.load_template("batch"),
            "powershell": self.load_template("powershell")
        }
        self.script_dir = Path("generated_scripts")
        self.script_dir.mkdir(exist_ok=True)
    
    def load_template(self, script_type):
        """Load script template from file"""
        template_path = Path(f"assets/scripts/template.{'bat' if script_type == 'batch' else 'ps1'}")
        
        if template_path.exists():
            with open(template_path, 'r') as f:
                return f.read()
        
        # Default templates
        if script_type == "batch":
            return """@echo off
REM Auto-generated script
REM Created: {timestamp}
REM Target: {target_ip}

echo Running script on %COMPUTERNAME%
echo IP Address: {target_ip}
echo Script purpose: {purpose}

{commands}

echo Script execution completed
pause
"""
        else:  # powershell
            return """# Auto-generated PowerShell script
# Created: {timestamp}
# Target: {target_ip}

Write-Host "Running script on $env:COMPUTERNAME"
Write-Host "IP Address: {target_ip}"
Write-Host "Script purpose: {purpose}"

{commands}

Write-Host "Script execution completed"
Read-Host "Press Enter to continue"
"""
    
    def generate_script(self, script_type, commands, target_ip, purpose="Administrative task"):
        """Generate a script for execution on target device"""
        timestamp = datetime.datetime.now().isoformat()
        
        # Format commands based on script type
        formatted_commands = []
        for command in commands:
            if command.strip():  # Skip empty lines
                if script_type == "batch":
                    formatted_commands.append(command)
                else:  # powershell
                    formatted_commands.append(f"Write-Host 'Executing: {command}'")
                    formatted_commands.append(f"try {{ {command} }}")
                    formatted_commands.append("catch { Write-Error $_.Exception.Message }")
        
        command_block = "\n".join(formatted_commands)
        
        # Replace placeholders in template
        script_content = self.script_templates[script_type].format(
            timestamp=timestamp,
            target_ip=target_ip,
            purpose=purpose,
            commands=command_block
        )
        
        # Generate filename
        filename = f"script_{target_ip}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{'bat' if script_type == 'batch' else 'ps1'}"
        filepath = self.script_dir / filename
        
        # Save script
        with open(filepath, 'w') as f:
            f.write(script_content)
        
        return {
            "filename": filename,
            "filepath": str(filepath),
            "content": script_content,
            "type": script_type
        }
    
    def get_common_scripts(self):
        """Return a list of common administrative scripts"""
        return {
            "system_info": {
                "name": "System Information",
                "type": "powershell",
                "commands": [
                    "systeminfo",
                    "Get-WmiObject -Class Win32_ComputerSystem | Select-Object Name, Manufacturer, Model",
                    "Get-WmiObject -Class Win32_OperatingSystem | Select-Object Caption, Version",
                    "ipconfig /all"
                ]
            },
            "disk_cleanup": {
                "name": "Disk Cleanup",
                "type": "batch",
                "commands": [
                    "cleanmgr /sagerun:1",
                    "echo Disk cleanup initiated"
                ]
            },
            "service_restart": {
                "name": "Restart Service",
                "type": "powershell",
                "commands": [
                    "Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Restart-Service -Force"
                ]
            },
            "software_inventory": {
                "name": "Software Inventory",
                "type": "powershell",
                "commands": [
                    "Get-WmiObject -Class Win32_Product | Select-Object Name, Version, Vendor | Format-Table -AutoSize"
                ]
            }
        }
    
    def execute_script_remotely(self, script_path, target_ip, username, password, script_type="powershell"):
        """Execute a script on a remote device"""
        try:
            from remote_control import RemoteControl
        except ImportError:
            return {"error": "RemoteControl module not found"}
        
        remote = RemoteControl()
        if remote.connect(target_ip, username, password):
            try:
                if script_type == "powershell":
                    # For PowerShell, we need to bypass execution policy
                    command = f"powershell -ExecutionPolicy Bypass -File \"{script_path}\""
                else:
                    command = f"cmd /c \"{script_path}\""
                
                result = remote.execute_command(command)
                return result
            finally:
                remote.disconnect()
        return {"error": "Failed to connect to remote host"}