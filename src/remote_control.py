import paramiko
import socket
import json

class RemoteControl:
    def __init__(self):
        self.ssh_client = None
    
    def connect(self, hostname, username, password, port=22):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, port, username, password, timeout=10)
            return True
        except (paramiko.AuthenticationException, 
                paramiko.SSHException, 
                socket.error,
                paramiko.BadHostKeyException) as e:
            print(f"Connection failed: {e}")
            return False
        except Exception as e:
            print(f"Unexpected connection error: {e}")
            return False
    
    def execute_command(self, command, timeout=30):
        if not self.ssh_client:
            return {"error": "Not connected to any host"}
        
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            exit_status = stdout.channel.recv_exit_status()
            
            return {
                "output": output,
                "error": error,
                "exit_status": exit_status,
                "success": exit_status == 0
            }
        except socket.timeout:
            return {"error": "Command execution timed out"}
        except Exception as e:
            return {"error": f"Command execution failed: {str(e)}"}
    
    def execute_script(self, script_path, interpreter="bash", timeout=60):
        """Execute a script file on the remote machine"""
        if not self.ssh_client:
            return {"error": "Not connected to any host"}
        
        try:
            # Upload and execute script
            sftp = self.ssh_client.open_sftp()
            remote_path = f"/tmp/script_{os.path.basename(script_path)}"
            sftp.put(script_path, remote_path)
            sftp.chmod(remote_path, 0o755)  # Make executable
            sftp.close()
            
            # Execute the script
            command = f"{interpreter} {remote_path}"
            result = self.execute_command(command, timeout)
            
            # Clean up
            self.execute_command(f"rm -f {remote_path}")
            
            return result
        except Exception as e:
            return {"error": f"Script execution failed: {str(e)}"}
    
    def disconnect(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
    
    def __del__(self):
        self.disconnect()