import subprocess
import xml.etree.ElementTree as ET
from nmap_device import NmapDevice

class NmapScanner:
    def __init__(self):
        self.devices = []
    
    def scan(self, target):
        """Perform an nmap scan on the target"""
        try:
            # Run nmap command
            command = ["nmap", "-O", "-sV", "-oX", "-", target]
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                return {"error": f"Nmap scan failed: {result.stderr}"}
            
            # Parse XML output
            return self.parse_nmap_xml(result.stdout)
        except subprocess.TimeoutExpired:
            return {"error": "Nmap scan timed out"}
        except FileNotFoundError:
            return {"error": "Nmap is not installed. Please install nmap to use this feature."}
        except Exception as e:
            return {"error": f"Scan failed: {str(e)}"}
    
    def parse_nmap_xml(self, xml_output):
        """Parse nmap XML output and extract device information"""
        try:
            root = ET.fromstring(xml_output)
            devices = []
            
            for host in root.findall("host"):
                device = NmapDevice()
                
                # Get IP address
                address = host.find("address[@addrtype='ipv4']")
                if address is not None:
                    device.ip_address = address.get("addr")
                
                # Get MAC address
                address = host.find("address[@addrtype='mac']")
                if address is not None:
                    device.mac_address = address.get("addr")
                    device.vendor = address.get("vendor", "")
                
                # Get hostname
                hostname = host.find("hostnames/hostname")
                if hostname is not None:
                    device.hostname = hostname.get("name")
                
                # Get OS information
                os_match = host.find("os/osmatch")
                if os_match is not None:
                    device.os = os_match.get("name")
                
                # Get port information
                ports = host.findall("ports/port")
                for port in ports:
                    port_id = port.get("portid")
                    state = port.find("state")
                    service = port.find("service")
                    
                    if state is not None and state.get("state") == "open":
                        port_info = {
                            "port": port_id,
                            "state": state.get("state"),
                            "service": service.get("name") if service is not None else "unknown",
                            "version": service.get("version") if service is not None else ""
                        }
                        device.open_ports.append(port_info)
                
                # Get status
                status = host.find("status")
                if status is not None:
                    device.status = status.get("state")
                
                devices.append(device)
            
            self.devices = devices
            return {"devices": [device.to_dict() for device in devices]}
        except ET.ParseError:
            return {"error": "Failed to parse nmap XML output"}