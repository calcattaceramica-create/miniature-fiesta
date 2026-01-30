#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Start Flask Server
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("=" * 80)
    print("🚀 Starting Flask Server...")
    print("=" * 80)
    print()
    print("Server running at: http://localhost:5000")
    print("Press CTRL+C to stop")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)

