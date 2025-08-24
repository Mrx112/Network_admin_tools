import socket
import subprocess
import platform
import netifaces
import threading
import os
from scapy.all import ARP, Ether, srp, conf

class NetworkManager:
    def __init__(self):
        self.devices = []
    
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    def get_network_interfaces(self):
        """Get all network interfaces"""
        interfaces = netifaces.interfaces()
        result = []
        
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    if 'addr' in addr and addr['addr'] != '127.0.0.1':
                        result.append({
                            'interface': interface,
                            'ip': addr['addr'],
                            'netmask': addr.get('netmask', '255.255.255.0')
                        })
        return result
    
    def calculate_network_range(self, ip, netmask):
        """Calculate network range from IP and netmask"""
        ip_parts = list(map(int, ip.split('.')))
        mask_parts = list(map(int, netmask.split('.')))
        
        network_parts = [ip_parts[i] & mask_parts[i] for i in range(4)]
        broadcast_parts = [network_parts[i] | (255 - mask_parts[i]) for i in range(4)]
        
        network_ip = '.'.join(map(str, network_parts))
        broadcast_ip = '.'.join(map(str, broadcast_parts))
        
        return f"{network_ip}/{'/'.join(netmask.split('.'))}"
    
    def ping_device(self, ip_address, timeout=1):
        """Ping a device with timeout"""
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", "-w", str(timeout * 1000), ip_address]
            return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
        except Exception:
            return False
    
    def arp_scan(self, network_range):
        """Perform ARP scan to discover devices on network"""
        devices = []
        try:
            # Check if we have permission to perform ARP scan
            if os.geteuid() != 0 and platform.system() != "Windows":
                return self.fallback_scan(network_range)
            
            # Create ARP packet
            arp = ARP(pdst=network_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            # Set timeout to prevent hanging
            conf.verb = 0  # Reduce verbosity
            
            # Send packet and get responses
            result = srp(packet, timeout=2, retry=1, verbose=0)[0]
            
            # Parse responses
            for sent, received in result:
                devices.append({
                    'ip': received.psrc,
                    'mac': received.hwsrc,
                    'vendor': self.get_vendor_from_mac(received.hwsrc),
                    'status': 'Online'
                })
        except Exception as e:
            print(f"ARP scan failed: {e}")
            # Fallback to ping scan if ARP scan fails
            devices = self.fallback_scan(network_range)
        
        return devices
    
    def fallback_scan(self, network_range):
        """Fallback scanning method using ping when ARP scan fails"""
        print("Using fallback ping scan method...")
        devices = []
        
        # Extract network base from range (e.g., 192.168.1.0/24 -> 192.168.1.)
        if '/' in network_range:
            base_ip = network_range.split('/')[0]
            network_base = '.'.join(base_ip.split('.')[:3]) + '.'
            
            # Scan first 20 IPs as a sample
            for i in range(1, 21):
                ip = f"{network_base}{i}"
                if self.ping_device(ip):
                    devices.append({
                        'ip': ip,
                        'mac': 'Unknown',
                        'vendor': 'Unknown',
                        'status': 'Online'
                    })
        else:
            # Single IP scan
            if self.ping_device(network_range):
                devices.append({
                    'ip': network_range,
                    'mac': 'Unknown',
                    'vendor': 'Unknown',
                    'status': 'Online'
                })
        
        return devices
    
    def get_vendor_from_mac(self, mac_address):
        """Get vendor from MAC address (first 3 bytes)"""
        # This is a simplified version - in practice you would use a MAC vendor database
        oui = mac_address[:8].upper()
        vendor_map = {
            "00:1C:42": "Parallels",
            "00:50:56": "VMware",
            "00:0C:29": "VMware",
            "00:1A:4B": "NVIDIA",
            "00:24:1D": "Cisco",
            "00:1B:21": "Intel",
            "00:1D:72": "Dell",
            "00:1E:4C": "Dell",
            "00:1F:29": "Dell",
            "00:21:9B": "HP",
            "00:25:B3": "Apple",
            "00:26:BB": "Apple",
            "00:30:65": "Apple",
            "00:A0:40": "Apple",
            "00:16:CB": "Apple",
            "00:19:E3": "Apple",
            "00:1C:B3": "Apple",
            "00:23:12": "Apple",
            "00:25:00": "Apple",
            "00:26:08": "Apple",
        }
        return vendor_map.get(oui, "Unknown")
    
    def get_network_info(self):
        try:
            hostname = socket.gethostname()
            local_ip = self.get_local_ip()
            interfaces = self.get_network_interfaces()
            
            return {
                "hostname": hostname,
                "local_ip": local_ip,
                "interfaces": interfaces
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_root_privileges(self):
        """Check if the application has root privileges"""
        if platform.system() == "Windows":
            # On Windows, we need to check for admin privileges
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            # On Unix systems, check for root
            return os.geteuid() == 0