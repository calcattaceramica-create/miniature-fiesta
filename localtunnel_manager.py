#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LocalTunnel Manager for DED ERP System
Manages LocalTunnel connections for global access
"""

import os
import sys
import subprocess
import time
import json
import socket
from pathlib import Path

class LocalTunnelManager:
    """Manages LocalTunnel connections"""
    
    def __init__(self):
        self.config_file = Path("localtunnel_config.json")
        self.port = 5000
        self.subdomain = None
        self.tunnel_process = None
        self.server_process = None
        
    def load_config(self):
        """Load saved configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.subdomain = config.get('subdomain')
                    self.port = config.get('port', 5000)
                    return True
            except Exception as e:
                print(f"⚠️  خطأ في قراءة الإعدادات: {e}")
        return False
    
    def save_config(self):
        """Save configuration"""
        try:
            config = {
                'subdomain': self.subdomain,
                'port': self.port
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"⚠️  خطأ في حفظ الإعدادات: {e}")
            return False
    
    def check_node_installed(self):
        """Check if Node.js is installed"""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, 
                                  text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def check_localtunnel_installed(self):
        """Check if LocalTunnel is installed"""
        try:
            result = subprocess.run(['lt', '--version'], 
                                  capture_output=True, 
                                  text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_localtunnel(self):
        """Install LocalTunnel"""
        print("\n📦 جاري تثبيت LocalTunnel...")
        print("⏳ قد يستغرق دقيقة...\n")
        
        try:
            result = subprocess.run(['npm', 'install', '-g', 'localtunnel'],
                                  capture_output=True,
                                  text=True)
            
            if result.returncode == 0:
                print("✅ تم تثبيت LocalTunnel بنجاح!\n")
                return True
            else:
                print(f"❌ فشل التثبيت: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ خطأ في التثبيت: {e}")
            return False
    
    def is_port_in_use(self, port):
        """Check if port is in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def start_server(self):
        """Start Flask server"""
        print("\n📡 جاري تشغيل السيرفر...")
        
        if self.is_port_in_use(self.port):
            print(f"✅ السيرفر يعمل بالفعل على المنفذ {self.port}")
            return True
        
        try:
            # Start server in background
            if sys.platform == 'win32':
                self.server_process = subprocess.Popen(
                    ['python', 'run.py'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                self.server_process = subprocess.Popen(
                    ['python', 'run.py'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Wait for server to start
            print("⏳ انتظار تشغيل السيرفر...")
            for i in range(10):
                time.sleep(1)
                if self.is_port_in_use(self.port):
                    print(f"✅ السيرفر يعمل على: http://localhost:{self.port}\n")
                    return True
            
            print("⚠️  السيرفر يستغرق وقتاً أطول من المعتاد...")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تشغيل السيرفر: {e}")
            return False
    
    def start_tunnel(self):
        """Start LocalTunnel"""
        print("\n🌍 جاري فتح النفق للعالم...")
        
        try:
            cmd = ['lt', '--port', str(self.port)]
            
            if self.subdomain:
                cmd.extend(['--subdomain', self.subdomain])
                url = f"https://{self.subdomain}.loca.lt"
            else:
                url = "https://[random].loca.lt"
            
            print(f"\n{'='*70}")
            print(f"🔗 رابطك: {url}")
            print(f"{'='*70}\n")
            
            # Start tunnel
            if sys.platform == 'win32':
                self.tunnel_process = subprocess.Popen(
                    cmd,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                self.tunnel_process = subprocess.Popen(cmd)
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في فتح النفق: {e}")
            return False
    
    def run(self):
        """Main run method"""
        print("\n" + "="*70)
        print("🏆 LocalTunnel Manager - DED ERP System")
        print("="*70 + "\n")
        
        # Check Node.js
        if not self.check_node_installed():
            print("❌ Node.js غير مثبت!")
            print("\n📥 يرجى تثبيت Node.js من: https://nodejs.org/")
            input("\nاضغط Enter للخروج...")
            return False
        
        print("✅ Node.js مثبت\n")
        
        # Check LocalTunnel
        if not self.check_localtunnel_installed():
            print("📦 LocalTunnel غير مثبت")
            install = input("هل تريد تثبيته الآن؟ (y/n): ")
            if install.lower() == 'y':
                if not self.install_localtunnel():
                    input("\nاضغط Enter للخروج...")
                    return False
            else:
                return False
        else:
            print("✅ LocalTunnel مثبت\n")
        
        # Load or create config
        if self.load_config() and self.subdomain:
            print(f"📋 الإعدادات المحفوظة:")
            print(f"   - الرابط: https://{self.subdomain}.loca.lt")
            use_saved = input("\nهل تريد استخدام نفس الرابط؟ (y/n): ")
            if use_saved.lower() != 'y':
                self.subdomain = None
        
        # Get subdomain if not set
        if not self.subdomain:
            print("\n" + "="*70)
            print("🎯 اختر نوع الرابط")
            print("="*70)
            print("\n1️⃣  رابط عشوائي (سريع)")
            print("   مثال: https://abc123.loca.lt")
            print("\n2️⃣  رابط مخصص (ثابت - موصى به!)")
            print("   مثال: https://myapp.loca.lt\n")
            
            choice = input("اختر (1 أو 2): ")
            
            if choice == '2':
                print("\n💡 اختر اسماً للرابط (حروف إنجليزية فقط، بدون مسافات)")
                print("   مثال: myapp, ded, myproject\n")
                self.subdomain = input("اسم الرابط: ").strip()
                
                if self.subdomain:
                    self.save_config()
                    print(f"\n✅ رابطك سيكون: https://{self.subdomain}.loca.lt\n")
        
        # Start server
        if not self.start_server():
            input("\nاضغط Enter للخروج...")
            return False
        
        # Start tunnel
        if not self.start_tunnel():
            input("\nاضغط Enter للخروج...")
            return False
        
        # Success message
        print("\n" + "="*70)
        print("✅ تم! النظام يعمل الآن!")
        print("="*70 + "\n")
        
        if self.subdomain:
            print(f"🔗 رابطك: https://{self.subdomain}.loca.lt\n")
        
        print("📋 معلومات تسجيل الدخول:")
        print("   Username: admin")
        print("   Password: admin123\n")
        
        print("⚠️  ملاحظات مهمة:")
        print("   - عند أول زيارة قد يطلب منك 'Click to Continue'")
        print("   - لا تغلق هذه النافذة!")
        print("   - لإيقاف النظام: اضغط CTRL+C\n")
        
        print("="*70)
        print("🎉 استمتع بالوصول من أي مكان في العالم!")
        print("="*70 + "\n")
        
        # Keep running
        try:
            input("اضغط Enter لإيقاف النظام...")
        except KeyboardInterrupt:
            print("\n\n⏹️  جاري إيقاف النظام...")
        
        return True

if __name__ == '__main__':
    manager = LocalTunnelManager()
    manager.run()

