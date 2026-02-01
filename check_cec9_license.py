#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models_license import License

app = create_app()

with app.app_context():
    # Check if license exists
    lic = License.query.filter_by(license_key='CEC9-79EE-C42F-2DAD').first()
    
    if lic:
        print(f"✅ License found: {lic.license_key}")
        print(f"   Client: {lic.client_name}")
        print(f"   Active: {lic.is_active}")
    else:
        print("❌ License CEC9-79EE-C42F-2DAD NOT FOUND!")
        
    # List all licenses
    print("\n📋 All licenses:")
    all_licenses = License.query.all()
    for l in all_licenses:
        print(f"   - {l.license_key}: {l.client_name}")

