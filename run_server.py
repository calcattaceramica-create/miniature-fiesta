#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple server runner
"""
from app import create_app

print("=" * 70)
print("DED ERP System - Starting Server...")
print("=" * 70)
print("")
print("Server URL: http://localhost:5000")
print("Username: admin")
print("Password: admin123")
print("")
print("Keep this window OPEN!")
print("Press CTRL+C to stop the server")
print("=" * 70)
print("")

app = create_app()
app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

