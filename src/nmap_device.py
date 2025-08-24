class NmapDevice:
    def __init__(self):
        self.ip_address = ""
        self.mac_address = ""
        self.hostname = ""
        self.os = ""
        self.status = ""
        self.vendor = ""
        self.open_ports = []
    
    def to_dict(self):
        return {
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "hostname": self.hostname,
            "os": self.os,
            "status": self.status,
            "vendor": self.vendor,
            "open_ports": self.open_ports
        }
    
    @staticmethod
    def from_dict(data):
        device = NmapDevice()
        device.ip_address = data.get("ip_address", "")
        device.mac_address = data.get("mac_address", "")
        device.hostname = data.get("hostname", "")
        device.os = data.get("os", "")
        device.status = data.get("status", "")
        device.vendor = data.get("vendor", "")
        device.open_ports = data.get("open_ports", [])
        return device