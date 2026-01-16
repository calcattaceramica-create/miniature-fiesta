#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple server starter for LocalTunnel
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    
    print("🚀 Starting Flask server...")
    print("📍 Server will run on: http://localhost:5000")
    print("⚠️  Do not close this window!")
    print("")
    
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")

