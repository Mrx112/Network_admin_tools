import subprocess
import os
import platform
import json

class ApplicationLauncher:
    def __init__(self):
        self.common_applications = self.load_common_applications()
    
    def load_common_applications(self):
        """Load a list of common applications with their paths"""
        applications = {}
        
        if platform.system() == "Windows":
            applications = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "browser": "chrome.exe",
                "explorer": "explorer.exe"
            }
        elif platform.system() == "Linux":
            applications = {
                "text_editor": "gedit",
                "terminal": "gnome-terminal",
                "browser": "firefox",
                "file_manager": "nautilus",
                "calculator": "gnome-calculator"
            }
        elif platform.system() == "Darwin":  # macOS
            applications = {
                "text_editor": "TextEdit",
                "terminal": "Terminal",
                "browser": "Safari",
                "finder": "Finder"
            }
        
        return applications
    
    def launch_local_application(self, app_name, arguments=""):
        """Launch an application on the local machine"""
        if app_name in self.common_applications:
            app_path = self.common_applications[app_name]
            try:
                if arguments:
                    subprocess.Popen([app_path] + arguments.split())
                else:
                    subprocess.Popen([app_path])
                return True
            except Exception as e:
                print(f"Failed to launch {app_name}: {e}")
                return False
        return False
    
    def launch_remote_application(self, target_ip, username, password, app_name, arguments=""):
        """Launch an application on a remote Windows machine using SSH"""
        try:
            from remote_control import RemoteControl
        except ImportError:
            return {"error": "RemoteControl module not found"}
        
        remote = RemoteControl()
        if remote.connect(target_ip, username, password):
            try:
                if app_name in self.common_applications:
                    app_path = self.common_applications[app_name]
                    command = f'"{app_path}"'
                    if arguments:
                        command += f' {arguments}'
                    
                    result = remote.execute_command(command)
                    return result
            finally:
                remote.disconnect()
        
        return {"error": "Failed to connect to remote host"}
    
    def get_installed_applications(self, target_ip, username, password):
        """Get list of installed applications on remote Windows machine"""
        try:
            from remote_control import RemoteControl
        except ImportError:
            return {"error": "RemoteControl module not found"}
        
        remote = RemoteControl()
        if remote.connect(target_ip, username, password):
            try:
                # Different commands for different OS
                if platform.system() == "Windows":
                    # PowerShell command to get installed applications
                    ps_command = """
                    Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* |
                    Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
                    Where-Object { $_.DisplayName -ne $null } |
                    ConvertTo-Json
                    """
                    result = remote.execute_command(f"powershell -Command \"{ps_command}\"")
                else:
                    # For Linux, get installed packages
                    result = remote.execute_command("dpkg-query -l | grep '^ii' | awk '{print $2 \" \" $3}'")
                
                if result and result.get("output"):
                    try:
                        if platform.system() == "Windows":
                            apps = json.loads(result["output"])
                        else:
                            apps = result["output"].split('\n')
                        return apps
                    except json.JSONDecodeError:
                        return result["output"].split('\n')
            finally:
                remote.disconnect()
        
        return {"error": "Failed to retrieve installed applications"}