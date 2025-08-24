#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import GUI
from enhanced_gui import EnhancedGUI
from network_manager import NetworkManager
from nmap_scanner import NmapScanner
from script_generator import ScriptGenerator
from application_launcher import ApplicationLauncher

def main():
    # Initialize network components
    network_manager = NetworkManager()
    nmap_scanner = NmapScanner()
    script_generator = ScriptGenerator()
    app_launcher = ApplicationLauncher()
    
    # Choose GUI version
    use_enhanced_gui = True
    
    if use_enhanced_gui:
        app = EnhancedGUI(network_manager, nmap_scanner, script_generator, app_launcher)
    else:
        app = GUI(network_manager)
    
    app.run()

if __name__ == "__main__":
    main()