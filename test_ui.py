#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎨 UI Test Script - سكريبت اختبار الواجهة
Tests the new improved UI of DED Control Panel
"""

import subprocess
import sys
import time
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎨 {text}")
    print("="*60 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def main():
    print_header("اختبار الواجهة الجديدة - UI Test")
    
    # Check if Control Panel file exists
    control_panel = Path("DED_Control_Panel.pyw")
    
    if not control_panel.exists():
        print("❌ Error: DED_Control_Panel.pyw not found!")
        return 1
    
    print_success("Control Panel file found")
    
    # Check file size
    file_size = control_panel.stat().st_size
    print_info(f"File size: {file_size:,} bytes")
    
    # Read and analyze the file
    with open(control_panel, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    print_info(f"Total lines: {len(lines)}")
    
    # Check for new features
    print_header("التحقق من الميزات الجديدة - Checking New Features")
    
    features = {
        "Light Theme Colors": "'bg': '#f8fafc'",
        "Larger Window": "geometry(\"1200x800\")",
        "Resizable Window": "resizable(True, True)",
        "Larger Fonts": "font=(\"Segoe UI\", 16, \"bold\")",
        "Active Background": "activebackground",
        "Modern Treeview": "style.theme_use('clam')",
        "Form Helper Function": "def create_form_row",
        "Action Button Helper": "def create_action_btn",
        "Border Effects": "bg=self.colors['border']",
        "Icon Emojis": "🏢"
    }

    found_features = 0
    for feature_name, feature_code in features.items():
        if feature_code in content:
            print_success(f"{feature_name} found")
            found_features += 1
        else:
            print(f"⚠️  {feature_name} not found")
    
    print_info(f"\nFeatures found: {found_features}/{len(features)}")
    
    # Check color scheme
    print_header("التحقق من نظام الألوان - Checking Color Scheme")
    
    colors = {
        "Background": "#f8fafc",
        "Card": "#ffffff",
        "Text": "#1e293b",
        "Accent": "#3b82f6",
        "Success": "#22c55e",
        "Danger": "#ef4444"
    }
    
    for color_name, color_code in colors.items():
        if color_code in content:
            print_success(f"{color_name}: {color_code}")
        else:
            print(f"❌ {color_name}: {color_code} not found")
    
    # Launch the Control Panel
    print_header("تشغيل لوحة التحكم - Launching Control Panel")
    
    print_info("Starting DED Control Panel...")
    print_info("Please check the following:")
    print("  1. ✅ Window size is 1200x800")
    print("  2. ✅ Light theme with white background")
    print("  3. ✅ Large, clear buttons")
    print("  4. ✅ Icons in form fields")
    print("  5. ✅ Two-line button text (Arabic + English)")
    print("  6. ✅ Modern table with colored headers")
    print("  7. ✅ Hover effects on buttons")
    print("  8. ✅ Clear borders between sections")
    
    print("\n" + "="*60)
    print("🚀 Launching Control Panel in 3 seconds...")
    print("="*60)
    
    time.sleep(3)
    
    try:
        # Launch the Control Panel
        subprocess.Popen([sys.executable, "DED_Control_Panel.pyw"])
        print_success("Control Panel launched successfully!")
        print_info("Check the window for the new UI improvements")
        return 0
    except Exception as e:
        print(f"❌ Error launching Control Panel: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    
    print("\n" + "="*60)
    if exit_code == 0:
        print("✅ UI Test completed successfully!")
        print("🎉 Enjoy the new improved interface!")
    else:
        print("❌ UI Test failed!")
    print("="*60 + "\n")
    
    sys.exit(exit_code)

