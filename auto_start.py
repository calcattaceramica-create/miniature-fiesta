#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auto Start Script - Starts Flask Server and LocalTunnel automatically
"""

import os
import sys
import subprocess
import time
import socket

def is_port_in_use(port):
    """Check if port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_server():
    """Start Flask server"""
    print("\n" + "="*70)
    print("🚀 Starting Flask Server...")
    print("="*70 + "\n")
    
    if is_port_in_use(5000):
        print("✅ Server is already running on port 5000\n")
        return True
    
    try:
        # Start server in new console
        if sys.platform == 'win32':
            subprocess.Popen(
                ['python', 'run.py'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            subprocess.Popen(['python', 'run.py'])
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(15):
            time.sleep(1)
            if is_port_in_use(5000):
                print("✅ Server is running on http://localhost:5000\n")
                return True
            print(f"   {i+1}/15 seconds...")
        
        print("⚠️  Server is taking longer than expected...")
        print("   But continuing anyway...\n")
        return True
        
    except Exception as e:
        print(f"❌ Error starting server: {e}\n")
        return False

def start_localtunnel():
    """Start LocalTunnel"""
    print("\n" + "="*70)
    print("🌍 Starting LocalTunnel...")
    print("="*70 + "\n")
    
    try:
        # Start LocalTunnel in new console
        if sys.platform == 'win32':
            subprocess.Popen(
                ['lt', '--port', '5000', '--subdomain', 'dedapp'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            subprocess.Popen(['lt', '--port', '5000', '--subdomain', 'dedapp'])
        
        print("✅ LocalTunnel started!\n")
        return True
        
    except Exception as e:
        print(f"❌ Error starting LocalTunnel: {e}\n")
        return False

def main():
    """Main function"""
    print("\n" + "="*70)
    print("🏆 DED ERP System - Auto Start")
    print("="*70 + "\n")
    
    # Start server
    if not start_server():
        print("❌ Failed to start server!")
        input("\nPress Enter to exit...")
        return
    
    # Wait a bit
    time.sleep(3)
    
    # Start LocalTunnel
    if not start_localtunnel():
        print("❌ Failed to start LocalTunnel!")
        input("\nPress Enter to exit...")
        return
    
    # Success message
    print("\n" + "="*70)
    print("✅ SUCCESS! System is running!")
    print("="*70 + "\n")
    
    print("🔗 Your URL: https://dedapp.loca.lt\n")
    
    print("📋 Login Credentials:")
    print("   Username: admin")
    print("   Password: admin123\n")
    
    print("🔑 Tunnel Password (first visit only):")
    print("   185.5.48.115\n")
    
    print("⚠️  Important Notes:")
    print("   - Two new windows opened (Server + LocalTunnel)")
    print("   - DO NOT close those windows!")
    print("   - Wait 10-15 seconds before opening the URL")
    print("   - On first visit, enter the tunnel password above\n")
    
    print("="*70)
    print("🎉 Enjoy your globally accessible ERP system!")
    print("="*70 + "\n")
    
    input("Press Enter to exit this window (Server and Tunnel will keep running)...")

if __name__ == '__main__':
    main()

