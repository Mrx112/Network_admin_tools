import tkinter as tk
from tkinter import ttk

class EnhancedNetworkTable(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create treeview with scrollbar
        columns = ("IP Address", "MAC Address", "Hostname", "Status", "OS", "Last Seen")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Add sample data
        self.add_sample_data()
    
    def add_sample_data(self):
        sample_data = [
            ("192.168.1.1", "00:11:22:33:44:55", "router", "Online", "Linux", "2023-05-15 10:30"),
            ("192.168.1.2", "AA:BB:CC:DD:EE:FF", "unknown", "Offline", "Unknown", "2023-05-14 15:45"),
            ("192.168.1.5", "11:22:33:44:55:66", "pc-01", "Online", "Windows", "2023-05-15 09:15"),
            ("192.168.1.10", "66:55:44:33:22:11", "laptop", "Online", "Windows", "2023-05-15 11:20"),
        ]
        
        for data in sample_data:
            self.tree.insert("", tk.END, values=data)