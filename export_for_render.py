#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export DED ERP System for Render Deployment
تصدير نظام DED ERP للنشر على Render
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_export():
    """Create export package for Render deployment"""
    
    print("=" * 70)
    print("📦 Exporting DED ERP System for Render Deployment")
    print("=" * 70)
    print()
    
    # Create export directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_name = f"DED_ERP_Render_{timestamp}"
    export_dir = Path(export_name)
    
    if export_dir.exists():
        shutil.rmtree(export_dir)
    
    export_dir.mkdir()
    print(f"✅ Created export directory: {export_dir}")
    
    # Files and directories to include
    include_items = [
        'app',
        'migrations',
        'translations',
        'config.py',
        'run.py',
        'requirements.txt',
        'render.yaml',
        'Procfile',
        'runtime.txt',
        'initialize_master_database.py',
        'README.md',
        'LICENSE',
    ]
    
    # Copy files
    print("\n📋 Copying files...")
    for item in include_items:
        src = Path(item)
        if src.exists():
            if src.is_file():
                shutil.copy2(src, export_dir / item)
                print(f"   ✓ {item}")
            elif src.is_dir():
                shutil.copytree(src, export_dir / item, 
                              ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo', '.DS_Store'))
                print(f"   ✓ {item}/")
        else:
            print(f"   ⚠ {item} not found, skipping...")
    
    # Create necessary directories
    print("\n📁 Creating necessary directories...")
    (export_dir / 'instance').mkdir(exist_ok=True)
    (export_dir / 'tenant_databases').mkdir(exist_ok=True)
    (export_dir / 'uploads' / 'products').mkdir(parents=True, exist_ok=True)
    print("   ✓ instance/")
    print("   ✓ tenant_databases/")
    print("   ✓ uploads/products/")
    
    # Create .gitkeep files
    (export_dir / 'uploads' / '.gitkeep').touch()
    (export_dir / 'uploads' / 'products' / '.gitkeep').touch()
    
    # Create deployment guide
    print("\n📖 Creating deployment guide...")
    deployment_guide = """# DED ERP System - Render Deployment Guide
دليل نشر نظام DED ERP على Render

## 🚀 Quick Start

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy on Render
1. Go to https://render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click "Apply" to deploy

### 3. Access Your Application
- Your app will be available at: `https://ded-inventory-system.onrender.com`
- Default credentials:
  - License Key: `RENDER-2026-PROD-LIVE`
  - Username: `admin`
  - Password: `admin123`

## 📋 What's Included

- ✅ Complete Flask application
- ✅ Multi-tenant license system
- ✅ SQLite database (no PostgreSQL needed)
- ✅ Automatic database initialization
- ✅ Production-ready configuration

## 🔧 Configuration

All configuration is in `render.yaml`:
- Python 3.11.7
- Gunicorn with 2 workers
- Frankfurt region (free tier)
- Automatic builds on push

## 📝 Notes

- Free tier includes 750 hours/month
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Database persists across deployments

## 🆘 Support

For issues or questions, check the logs in Render dashboard.

---
Created: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
"""
    
    (export_dir / 'DEPLOYMENT_GUIDE.md').write_text(deployment_guide, encoding='utf-8')
    print("   ✓ DEPLOYMENT_GUIDE.md")
    
    # Create ZIP file
    print("\n📦 Creating ZIP archive...")
    zip_filename = f"{export_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(export_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"   ✓ {zip_filename}")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    shutil.rmtree(export_dir)
    print("   ✓ Temporary directory removed")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ Export Complete!")
    print("=" * 70)
    print(f"\n📦 Package: {zip_filename}")
    print(f"📏 Size: {os.path.getsize(zip_filename) / 1024 / 1024:.2f} MB")
    print("\n📖 Next Steps:")
    print("   1. Extract the ZIP file")
    print("   2. Follow instructions in DEPLOYMENT_GUIDE.md")
    print("   3. Push to GitHub and deploy on Render")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    create_export()

