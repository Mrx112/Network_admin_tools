import socket
import platform
import uuid

class DeviceInfo:
    def __init__(self, ip_address, mac_address="", hostname="", os_type="", status="Unknown"):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.hostname = hostname
        self.os_type = os_type
        self.status = status
        self.open_ports = []
        self.services = {}
        self.last_seen = None
    
    def to_dict(self):
        return {
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "hostname": self.hostname,
            "os_type": self.os_type,
            "status": self.status,
            "open_ports": self.open_ports,
            "services": self.services,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None
        }
    
    @staticmethod
    def from_dict(data):
        device = DeviceInfo(
            data.get("ip_address", ""),
            data.get("mac_address", ""),
            data.get("hostname", ""),
            data.get("os_type", ""),
            data.get("status", "Unknown")
        )
        device.open_ports = data.get("open_ports", [])
        device.services = data.get("services", {})
        
        if data.get("last_seen"):
            from datetime import datetime
            device.last_seen = datetime.fromisoformat(data["last_seen"])
        
        return device
    
    def get_device_fingerprint(self):
        """Generate a unique fingerprint for the device"""
        import hashlib
        fingerprint_data = f"{self.ip_address}-{self.mac_address}-{self.hostname}"
        return hashlib.md5(fingerprint_data.encode()).hexdigest()