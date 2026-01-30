#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Clear all Flask sessions
مسح جميع جلسات Flask
"""

import os
import shutil
from pathlib import Path

def clear_sessions():
    """Clear all session files"""
    print("=" * 70)
    print("🧹 Clearing all Flask sessions")
    print("=" * 70)
    print()
    
    # Flask-Session stores sessions in flask_session directory
    session_dir = Path('flask_session')
    
    if session_dir.exists():
        try:
            shutil.rmtree(session_dir)
            print(f"✅ Deleted session directory: {session_dir}")
        except Exception as e:
            print(f"❌ Error deleting session directory: {e}")
    else:
        print(f"⏭️  Session directory not found: {session_dir}")
    
    print()
    print("=" * 70)
    print("✅ Sessions cleared!")
    print("=" * 70)
    print()
    print("📝 Next steps:")
    print("1. Restart the Flask server (Ctrl+C then python run.py)")
    print("2. Clear browser cache (Ctrl+Shift+Delete)")
    print("3. Close all browser windows")
    print("4. Open browser and login again")
    print()

if __name__ == '__main__':
    clear_sessions()

