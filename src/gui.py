import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class GUI:
    def __init__(self, network_manager):
        self.network_manager = network_manager
        self.root = tk.Tk()
        self.root.title("Network Admin Tool")
        self.root.geometry("800x600")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Network Info Tab
        self.network_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.network_frame, text="Network Info")
        self.setup_network_tab()
        
        # File Transfer Tab
        self.file_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.file_frame, text="File Transfer")
        self.setup_file_transfer_tab()
        
        # Remote Control Tab
        self.remote_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.remote_frame, text="Remote Control")
        self.setup_remote_control_tab()
    
    def setup_network_tab(self):
        # Local network info
        ttk.Label(self.network_frame, text="Local Network Information", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        network_info = self.network_manager.get_network_info()
        
        ttk.Label(self.network_frame, text="Hostname:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.network_frame, text=network_info.get("hostname", "Unknown")).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.network_frame, text="IP Address:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.network_frame, text=network_info.get("local_ip", "Unknown")).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Ping section
        ttk.Label(self.network_frame, text="Ping Device", 
                 font=("Arial", 14, "bold")).grid(row=3, column=0, columnspan=2, pady=(20, 10))
        
        ttk.Label(self.network_frame, text="IP Address:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.ping_ip = ttk.Entry(self.network_frame, width=15)
        self.ping_ip.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        self.ping_result = ttk.Label(self.network_frame, text="")
        self.ping_result.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.network_frame, text="Ping", 
                  command=self.do_ping).grid(row=6, column=0, columnspan=2, pady=10)
    
    def setup_file_transfer_tab(self):
        ttk.Label(self.file_frame, text="File Transfer (SSH)", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Connection details
        ttk.Label(self.file_frame, text="Host:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ftp_host = ttk.Entry(self.file_frame, width=20)
        self.ftp_host.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.file_frame, text="Username:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ftp_user = ttk.Entry(self.file_frame, width=20)
        self.ftp_user.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.file_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.ftp_pass = ttk.Entry(self.file_frame, width=20, show="*")
        self.ftp_pass.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # File operations
        ttk.Button(self.file_frame, text="Upload File", 
                  command=self.upload_file).grid(row=4, column=0, pady=10)
        ttk.Button(self.file_frame, text="Download File", 
                  command=self.download_file).grid(row=4, column=1, pady=10)
        
        self.ftp_status = ttk.Label(self.file_frame, text="")
        self.ftp_status.grid(row=5, column=0, columnspan=2, pady=5)
    
    def setup_remote_control_tab(self):
        ttk.Label(self.remote_frame, text="Remote Command Execution", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Connection details
        ttk.Label(self.remote_frame, text="Host:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.remote_host = ttk.Entry(self.remote_frame, width=20)
        self.remote_host.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.remote_frame, text="Username:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.remote_user = ttk.Entry(self.remote_frame, width=20)
        self.remote_user.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.remote_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.remote_pass = ttk.Entry(self.remote_frame, width=20, show="*")
        self.remote_pass.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Command execution
        ttk.Label(self.remote_frame, text="Command:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.command_entry = ttk.Entry(self.remote_frame, width=30)
        self.command_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(self.remote_frame, text="Execute", 
                  command=self.execute_remote).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Output area
        ttk.Label(self.remote_frame, text="Output:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.output_text = tk.Text(self.remote_frame, height=10, width=50)
        self.output_text.grid(row=7, column=0, columnspan=2, pady=5)
    
    def do_ping(self):
        ip = self.ping_ip.get()
        if not ip:
            messagebox.showerror("Error", "Please enter an IP address")
            return
        
        is_online = self.network_manager.ping_device(ip)
        if is_online:
            self.ping_result.config(text=f"{ip} is online", foreground="green")
        else:
            self.ping_result.config(text=f"{ip} is offline", foreground="red")
    
    def upload_file(self):
        messagebox.showinfo("Info", "Upload functionality would be implemented here")
    
    def download_file(self):
        messagebox.showinfo("Info", "Download functionality would be implemented here")
    
    def execute_remote(self):
        messagebox.showinfo("Info", "Remote execution functionality would be implemented here")
    
    def run(self):
        self.root.mainloop()