#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Production server using Waitress
This is a production-ready WSGI server for Windows
"""
import os
from waitress import serve
from app import create_app

# Create the Flask application
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    print("=" * 60)
    print("Starting DED ERP System - Production Server")
    print("=" * 60)
    print(f"Server: Waitress WSGI Server")
    print(f"Host: 0.0.0.0")
    print(f"Port: 5000")
    print(f"URL: http://127.0.0.1:5000")
    print(f"URL: http://localhost:5000")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Serve the application
    # threads=4 means it can handle 4 concurrent requests
    # channel_timeout=300 means 5 minutes timeout for long requests
    serve(app, 
          host='0.0.0.0', 
          port=5000, 
          threads=4,
          channel_timeout=300,
          cleanup_interval=30,
          asyncore_use_poll=True)

