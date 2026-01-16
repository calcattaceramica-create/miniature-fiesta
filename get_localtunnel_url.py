#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get LocalTunnel URL
"""

import subprocess
import time
import re

print("🔍 Checking LocalTunnel status...")
print("")

# Try to get the URL from the process
try:
    # Start LocalTunnel and capture output
    process = subprocess.Popen(
        ['lt', '--port', '5000', '--subdomain', 'dedapp'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    print("⏳ Waiting for LocalTunnel to start...")
    time.sleep(3)
    
    # Read output
    output = process.stdout.readline()
    
    if output:
        print("✅ LocalTunnel Output:")
        print(output)
        
        # Extract URL
        url_match = re.search(r'https://[^\s]+', output)
        if url_match:
            url = url_match.group(0)
            print("")
            print("═" * 80)
            print("🎉 YOUR PUBLIC URL:")
            print(f"   {url}")
            print("═" * 80)
            print("")
            print("✅ Open this URL in any browser from anywhere in the world!")
            print("✅ Login: admin / admin123")
            print("")
    else:
        print("⚠️  No output yet. LocalTunnel might still be starting...")
        
except Exception as e:
    print(f"❌ Error: {e}")
    
input("Press Enter to exit...")

