#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple server starter for DED ERP System
"""
import os
import sys

def main():
    print("=" * 50)
    print("🚀 Starting DED ERP Server")
    print("=" * 50)
    print()
    print("📍 Server URL: http://localhost:5000")
    print("👤 Username: admin")
    print("🔑 Password: admin123")
    print()
    print("⚠️  Keep this window open!")
    print("   Press CTRL+C to stop the server")
    print("=" * 50)
    print()
    
    # Import and run the app
    from app import create_app
    app = create_app()
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()

