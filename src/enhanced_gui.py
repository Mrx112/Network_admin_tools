import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from gui import GUI
from enhanced_network_table import EnhancedNetworkTable
import json
import threading

class EnhancedGUI(GUI):
    def __init__(self, network_manager, nmap_scanner, script_generator, app_launcher):
        super().__init__(network_manager)
        self.nmap_scanner = nmap_scanner
        self.script_generator = script_generator
        self.app_launcher = app_launcher
        self.root.title("Enhanced Network Admin Tool")
        self.scanning = False
        
        # Add additional tabs
        self.setup_enhanced_tabs()
    
    def setup_enhanced_tabs(self):
        # Network Scan Tab
        self.scan_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.scan_frame, text="Network Scan")
        self.setup_scan_tab()
        
        # Enhanced Network Table Tab
        self.enhanced_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.enhanced_frame, text="Network Devices")
        self.setup_network_devices_tab()
        
        # Script Generator Tab
        self.script_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.script_frame, text="Script Generator")
        self.setup_script_tab()
        
        # Application Launcher Tab
        self.app_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.app_frame, text="Application Launcher")
        self.setup_app_launcher_tab()
    
    def setup_scan_tab(self):
        ttk.Label(self.scan_frame, text="Network Scanner", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Network interface selection
        ttk.Label(self.scan_frame, text="Network Interface:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(self.scan_frame, textvariable=self.interface_var, width=30)
        self.interface_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Refresh interfaces button
        ttk.Button(self.scan_frame, text="Refresh Interfaces", 
                  command=self.refresh_interfaces).grid(row=1, column=2, padx=5)
        
        # Target selection
        ttk.Label(self.scan_frame, text="Target IP Range:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.scan_range = ttk.Entry(self.scan_frame, width=30)
        self.scan_range.insert(0, "192.168.1.0/24")
        self.scan_range.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Scan options
        ttk.Label(self.scan_frame, text="Scan Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.scan_type = ttk.Combobox(self.scan_frame, values=["Quick Scan", "Full Scan", "OS Detection", "Service Detection"])
        self.scan_type.set("Quick Scan")
        self.scan_type.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Scan button
        ttk.Button(self.scan_frame, text="Scan Network", 
                  command=self.start_scan_thread).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Progress bar
        self.scan_progress = ttk.Progressbar(self.scan_frame, mode='indeterminate')
        self.scan_progress.grid(row=5, column=0, columnspan=3, sticky=tk.EW, pady=5)
        
        # Scan results
        ttk.Label(self.scan_frame, text="Scan Results:").grid(row=6, column=0, sticky=tk.W, pady=5)
        
        # Treeview for results
        columns = ("IP", "MAC", "Hostname", "Status", "OS", "Ports")
        self.scan_tree = ttk.Treeview(self.scan_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.scan_tree.heading(col, text=col)
            self.scan_tree.column(col, width=100)
        
        self.scan_tree.grid(row=7, column=0, columnspan=3, pady=5, sticky="nsew")
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.scan_frame, orient=tk.VERTICAL, command=self.scan_tree.yview)
        self.scan_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=7, column=3, sticky="ns")
        
        # Action buttons for selected device
        ttk.Button(self.scan_frame, text="Ping Selected", 
                  command=self.ping_selected).grid(row=8, column=0, pady=10)
        ttk.Button(self.scan_frame, text="Get Details", 
                  command=self.get_device_details).grid(row=8, column=1, pady=10)
        ttk.Button(self.scan_frame, text="Remote Desktop", 
                  command=self.remote_desktop).grid(row=8, column=2, pady=10)
        
        # Configure grid weights for resizing
        self.scan_frame.grid_rowconfigure(7, weight=1)
        self.scan_frame.grid_columnconfigure(1, weight=1)
        
        # Load interfaces
        self.refresh_interfaces()
    
    def setup_network_devices_tab(self):
        ttk.Label(self.enhanced_frame, text="Network Devices Table", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create enhanced network table
        self.network_table = EnhancedNetworkTable(self.enhanced_frame)
        self.network_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        ttk.Button(self.enhanced_frame, text="Refresh", 
                  command=self.refresh_network_table).pack(pady=10)
    
    def setup_script_tab(self):
        ttk.Label(self.script_frame, text="Script Generator", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Target selection
        ttk.Label(self.script_frame, text="Target IP:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.script_target_ip = ttk.Entry(self.script_frame, width=20)
        self.script_target_ip.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Script type selection
        ttk.Label(self.script_frame, text="Script Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.script_type = ttk.Combobox(self.script_frame, values=["powershell", "batch"])
        self.script_type.set("powershell")
        self.script_type.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Predefined scripts
        ttk.Label(self.script_frame, text="Predefined Scripts:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.preset_script = ttk.Combobox(self.script_frame, width=20)
        self.preset_script.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Load predefined scripts
        common_scripts = self.script_generator.get_common_scripts()
        self.preset_script['values'] = [f"{name} ({info['name']})" for name, info in common_scripts.items()]
        
        # Load script button
        ttk.Button(self.script_frame, text="Load Script", 
                  command=self.load_preset_script).grid(row=3, column=2, padx=5)
        
        # Script purpose
        ttk.Label(self.script_frame, text="Script Purpose:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.script_purpose = ttk.Entry(self.script_frame, width=30)
        self.script_purpose.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Script commands
        ttk.Label(self.script_frame, text="Commands (one per line):").grid(row=5, column=0, sticky=tk.NW, pady=5)
        self.script_commands = scrolledtext.ScrolledText(self.script_frame, width=40, height=10)
        self.script_commands.grid(row=5, column=1, columnspan=2, pady=5, sticky="nsew")
        
        # Generate and execute buttons
        ttk.Button(self.script_frame, text="Generate Script", 
                  command=self.generate_script).grid(row=6, column=0, pady=10)
        ttk.Button(self.script_frame, text="Execute Remotely", 
                  command=self.execute_script_remotely).grid(row=6, column=1, pady=10)
        ttk.Button(self.script_frame, text="Save Script", 
                  command=self.save_script).grid(row=6, column=2, pady=10)
        
        # Script output
        ttk.Label(self.script_frame, text="Output:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.script_output = scrolledtext.ScrolledText(self.script_frame, width=40, height=8)
        self.script_output.grid(row=8, column=0, columnspan=3, pady=5, sticky="nsew")
        
        # Configure grid weights
        self.script_frame.grid_rowconfigure(5, weight=1)
        self.script_frame.grid_rowconfigure(8, weight=1)
        self.script_frame.grid_columnconfigure(1, weight=1)
    
    def setup_app_launcher_tab(self):
        ttk.Label(self.app_frame, text="Application Launcher", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Target selection
        ttk.Label(self.app_frame, text="Target IP:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.app_target_ip = ttk.Entry(self.app_frame, width=20)
        self.app_target_ip.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Credentials
        ttk.Label(self.app_frame, text="Username:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.app_username = ttk.Entry(self.app_frame, width=20)
        self.app_username.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.app_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.app_password = ttk.Entry(self.app_frame, width=20, show="*")
        self.app_password.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Application selection
        ttk.Label(self.app_frame, text="Application:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.app_selection = ttk.Combobox(self.app_frame, width=20)
        self.app_selection['values'] = list(self.app_launcher.common_applications.keys())
        self.app_selection.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Arguments
        ttk.Label(self.app_frame, text="Arguments:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.app_arguments = ttk.Entry(self.app_frame, width=30)
        self.app_arguments.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Launch buttons
        ttk.Button(self.app_frame, text="Launch Locally", 
                  command=self.launch_local_app).grid(row=6, column=0, pady=10)
        ttk.Button(self.app_frame, text="Launch Remotely", 
                  command=self.launch_remote_app).grid(row=6, column=1, pady=10)
        ttk.Button(self.app_frame, text="Get Installed Apps", 
                  command=self.get_installed_apps).grid(row=6, column=2, pady=10)
        
        # Application output
        ttk.Label(self.app_frame, text="Output:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.app_output = scrolledtext.ScrolledText(self.app_frame, width=40, height=10)
        self.app_output.grid(row=8, column=0, columnspan=3, pady=5, sticky="nsew")
        
        # Configure grid weights
        self.app_frame.grid_rowconfigure(8, weight=1)
        self.app_frame.grid_columnconfigure(1, weight=1)
    
    def check_privileges(self):
        """Check if we have sufficient privileges for scanning"""
        has_privileges = self.network_manager.check_root_privileges()
        
        if not has_privileges:
            messagebox.showwarning(
                "Privileges Warning", 
                "Network scanning features are limited without root/administrator privileges.\n\n"
                "On Linux/macOS, run with: sudo python3 main.py\n"
                "On Windows, run as Administrator"
            )
        return has_privileges
    
    def refresh_interfaces(self):
        """Refresh network interfaces list"""
        interfaces = self.network_manager.get_network_interfaces()
        interface_list = [f"{iface['interface']} ({iface['ip']})" for iface in interfaces]
        self.interface_combo['values'] = interface_list
        if interface_list:
            self.interface_combo.set(interface_list[0])
    
    def start_scan_thread(self):
        """Start network scan in a separate thread"""
        if self.scanning:
            messagebox.showwarning("Warning", "Scan already in progress")
            return
        
        # Check privileges
        self.check_privileges()
        
        self.scanning = True
        self.scan_progress.start()
        threading.Thread(target=self.scan_network, daemon=True).start()
    
    def scan_network(self):
        """Perform network scan"""
        target = self.scan_range.get()
        if not target:
            self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a target IP range"))
            self.scanning = False
            self.scan_progress.stop()
            return
        
        # Clear previous results
        self.root.after(0, lambda: [self.scan_tree.delete(item) for item in self.scan_tree.get_children()])
        
        # Perform scan based on type
        scan_type = self.scan_type.get()
        
        if scan_type == "Quick Scan":
            devices = self.network_manager.arp_scan(target)
        else:
            # For more advanced scans, use nmap
            result = self.nmap_scanner.scan(target)
            if "error" in result:
                self.root.after(0, lambda: messagebox.showerror("Error", result["error"]))
                self.scanning = False
                self.scan_progress.stop()
                return
            devices = result.get("devices", [])
        
        # Add devices to treeview
        for device in devices:
            self.root.after(0, lambda d=device: self.scan_tree.insert("", tk.END, values=(
                d.get("ip", ""),
                d.get("mac", ""),
                d.get("hostname", ""),
                d.get("status", ""),
                d.get("os", ""),
                len(d.get("open_ports", []))
            )))
        
        self.root.after(0, lambda: messagebox.showinfo("Scan Complete", f"Found {len(devices)} devices"))
        self.scanning = False
        self.scan_progress.stop()
    
    def load_preset_script(self):
        """Load a predefined script"""
        selected = self.preset_script.get()
        if not selected:
            return
        
        script_name = selected.split(" ")[0]
        common_scripts = self.script_generator.get_common_scripts()
        
        if script_name in common_scripts:
            script = common_scripts[script_name]
            self.script_type.set(script["type"])
            self.script_purpose.delete(0, tk.END)
            self.script_purpose.insert(0, script["name"])
            
            # Clear and add commands
            self.script_commands.delete(1.0, tk.END)
            for command in script["commands"]:
                self.script_commands.insert(tk.END, command + "\n")
    
    def generate_script(self):
        """Generate a script from the entered commands"""
        target_ip = self.script_target_ip.get()
        script_type = self.script_type.get()
        purpose = self.script_purpose.get()
        commands = self.script_commands.get(1.0, tk.END).strip().split('\n')
        
        if not target_ip or not commands:
            messagebox.showerror("Error", "Please enter target IP and at least one command")
            return
        
        result = self.script_generator.generate_script(script_type, commands, target_ip, purpose)
        
        self.script_output.delete(1.0, tk.END)
        self.script_output.insert(tk.END, f"Script generated: {result['filename']}\n\n")
        self.script_output.insert(tk.END, result['content'])
        
        messagebox.showinfo("Success", f"Script generated: {result['filename']}")
    
    def execute_script_remotely(self):
        """Execute the generated script on a remote machine"""
        target_ip = self.script_target_ip.get()
        script_type = self.script_type.get()
        
        if not target_ip:
            messagebox.showerror("Error", "Please enter target IP")
            return
        
        # For this example, we'll just show a dialog asking for credentials
        from tkinter.simpledialog import askstring
        
        username = askstring("Credentials", "Enter username for remote machine:")
        if not username:
            return
        
        password = askstring("Credentials", "Enter password:", show='*')
        if not password:
            return
        
        # In a real implementation, you would use the script generator to execute the script
        # For now, we'll just show a message
        messagebox.showinfo("Info", f"Would execute script on {target_ip} as {username}")
    
    def save_script(self):
        """Save the generated script to a file"""
        # This would be implemented to save the script content to a file
        messagebox.showinfo("Info", "Script save functionality would be implemented here")
    
    def launch_local_app(self):
        """Launch an application locally"""
        app_name = self.app_selection.get()
        arguments = self.app_arguments.get()
        
        if not app_name:
            messagebox.showerror("Error", "Please select an application")
            return
        
        success = self.app_launcher.launch_local_application(app_name, arguments)
        if success:
            self.app_output.insert(tk.END, f"Launched {app_name} locally\n")
        else:
            self.app_output.insert(tk.END, f"Failed to launch {app_name} locally\n")
    
    def launch_remote_app(self):
        """Launch an application on a remote machine"""
        target_ip = self.app_target_ip.get()
        username = self.app_username.get()
        password = self.app_password.get()
        app_name = self.app_selection.get()
        arguments = self.app_arguments.get()
        
        if not all([target_ip, username, password, app_name]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        # Tampilkan progress indicator
        self.app_output.delete(1.0, tk.END)
        self.app_output.insert(tk.END, f"Attempting to launch {app_name} on {target_ip}...\n")
        self.app_output.update()
        
        try:
            result = self.app_launcher.launch_remote_application(target_ip, username, password, app_name, arguments)
            
            self.app_output.delete(1.0, tk.END)
            if result:
                if result.get("output"):
                    self.app_output.insert(tk.END, f"Output:\n{result['output']}\n")
                if result.get("error"):
                    self.app_output.insert(tk.END, f"Error:\n{result['error']}\n")
                if result.get("exit_status") is not None:
                    self.app_output.insert(tk.END, f"Exit Status: {result['exit_status']}\n")
            else:
                self.app_output.insert(tk.END, "Failed to launch application remotely\n")
        except Exception as e:
            self.app_output.insert(tk.END, f"Exception occurred: {str(e)}\n")
    
    def get_installed_apps(self):
        """Get installed applications from remote machine"""
        target_ip = self.app_target_ip.get()
        username = self.app_username.get()
        password = self.app_password.get()
        
        if not all([target_ip, username, password]):
            messagebox.showerror("Error", "Please enter target IP, username and password")
            return
        
        apps = self.app_launcher.get_installed_applications(target_ip, username, password)
        
        self.app_output.delete(1.0, tk.END)
        if apps:
            if isinstance(apps, list):
                self.app_output.insert(tk.END, "Installed applications:\n")
                for app in apps:
                    self.app_output.insert(tk.END, f"- {app}\n")
            else:
                self.app_output.insert(tk.END, "Installed applications (JSON):\n")
                self.app_output.insert(tk.END, json.dumps(apps, indent=2))
        else:
            self.app_output.insert(tk.END, "No applications found or failed to retrieve\n")
    
    def ping_selected(self):
        """Ping the selected device"""
        selection = self.scan_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a device first")
            return
        
        item = self.scan_tree.item(selection[0])
        ip_address = item['values'][0]
        
        is_online = self.network_manager.ping_device(ip_address)
        if is_online:
            messagebox.showinfo("Ping Result", f"{ip_address} is online")
        else:
            messagebox.showinfo("Ping Result", f"{ip_address} is offline")
    
    def get_device_details(self):
        """Get details for the selected device"""
        selection = self.scan_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a device first")
            return
        
        item = self.scan_tree.item(selection[0])
        ip_address = item['values'][0]
        
        # For this example, we'll just show a simple message
        messagebox.showinfo("Device Details", f"Would show details for {ip_address}")
    
    def remote_desktop(self):
        """Initiate remote desktop connection to selected device"""
        selection = self.scan_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a device first")
            return
        
        item = self.scan_tree.item(selection[0])
        ip_address = item['values'][0]
        
        # For this example, we'll just show a message
        messagebox.showinfo("Remote Desktop", f"Would initiate RDP to {ip_address}")
    
    def refresh_network_table(self):
        """Refresh the network devices table"""
        # This would refresh the network table with current data
        messagebox.showinfo("Info", "Network table refresh would be implemented here")