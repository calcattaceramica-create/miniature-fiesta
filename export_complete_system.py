#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete Export of DED ERP System with License Management
تصدير كامل لنظام DED ERP مع إدارة التراخيص
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_complete_export():
    """Create complete export package with all documentation"""
    
    print("=" * 80)
    print("📦 DED ERP System - Complete Export with License Management")
    print("   تصدير كامل لنظام DED ERP مع إدارة التراخيص")
    print("=" * 80)
    print()
    
    # Create export directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_name = f"DED_ERP_Complete_{timestamp}"
    export_dir = Path(export_name)
    
    if export_dir.exists():
        shutil.rmtree(export_dir)
    
    export_dir.mkdir()
    print(f"✅ Created export directory: {export_dir}")
    print()
    
    # Files and directories to include
    include_items = {
        'Core Application': [
            'app',
            'migrations',
            'translations',
            'config.py',
            'run.py',
        ],
        'Dependencies': [
            'requirements.txt',
            'runtime.txt',
        ],
        'Deployment': [
            'render.yaml',
            'Procfile',
            'initialize_master_database.py',
        ],
        'Documentation': [
            'README.md',
            'LICENSE',
            'RENDER_DEPLOYMENT.md',
            'EXPORT_README.md',
        ],
    }
    
    # Copy files by category
    for category, items in include_items.items():
        print(f"📋 {category}:")
        for item in items:
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
        print()
    
    # Create necessary directories
    print("📁 Creating necessary directories...")
    dirs_to_create = [
        'instance',
        'tenant_databases',
        'uploads/products',
        'logs',
    ]
    
    for dir_path in dirs_to_create:
        (export_dir / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {dir_path}/")
    print()
    
    # Create .gitkeep files
    print("📝 Creating .gitkeep files...")
    gitkeep_dirs = [
        'instance',
        'tenant_databases',
        'uploads',
        'uploads/products',
        'logs',
    ]
    
    for dir_path in gitkeep_dirs:
        (export_dir / dir_path / '.gitkeep').touch()
        print(f"   ✓ {dir_path}/.gitkeep")
    print()
    
    # Create comprehensive README
    print("📖 Creating comprehensive README...")
    readme_content = f"""# DED ERP System - Complete Package
# نظام DED ERP - الحزمة الكاملة

**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 What's Included

This package contains:
- ✅ Complete DED ERP System
- ✅ Multi-Tenant License Management
- ✅ Ready for Render Deployment
- ✅ Complete Documentation
- ✅ Default Production License

## 🚀 Quick Start

### Option 1: Deploy to Render (Recommended)

1. **Extract this package**
2. **Read `RENDER_DEPLOYMENT.md`**
3. **Push to GitHub**
4. **Deploy on Render**

### Option 2: Run Locally

```bash
pip install -r requirements.txt
python initialize_master_database.py
python run.py
```

## 📚 Documentation

- `RENDER_DEPLOYMENT.md` - Complete deployment guide
- `EXPORT_README.md` - Package contents and features
- `README.md` - Application documentation

## 🔑 Default License

```
License Key: RENDER-2026-PROD-LIVE
Username: admin
Password: admin123
Type: Lifetime
```

## 📊 License Management

Access at: `/security/licenses`

Features:
- Create new licenses
- Manage existing licenses
- Suspend/Activate licenses
- Multi-tenant isolation

## 🆘 Support

For help, check the documentation files or contact support.

---

**DED ERP System** - Professional Business Management
"""
    
    (export_dir / 'START_HERE.md').write_text(readme_content, encoding='utf-8')
    print("   ✓ START_HERE.md")
    print()
    
    # Create .gitignore
    print("📝 Creating .gitignore...")
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/

# Virtual Environment
venv/
env/

# Database (keep structure, ignore data)
*.db
!.gitkeep

# Logs
*.log
logs/*
!logs/.gitkeep

# Uploads
uploads/*
!uploads/.gitkeep
!uploads/products/.gitkeep

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
.DS_Store
"""
    
    (export_dir / '.gitignore').write_text(gitignore_content, encoding='utf-8')
    print("   ✓ .gitignore")
    print()
    
    # Create ZIP file
    print("📦 Creating ZIP archive...")
    zip_filename = f"{export_name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(export_dir.parent)
                zipf.write(file_path, arcname)
                
    file_size = os.path.getsize(zip_filename) / 1024 / 1024
    print(f"   ✓ {zip_filename} ({file_size:.2f} MB)")
    print()
    
    # Cleanup
    print("🧹 Cleaning up temporary files...")
    shutil.rmtree(export_dir)
    print("   ✓ Temporary directory removed")
    print()
    
    # Final summary
    print("=" * 80)
    print("✅ EXPORT COMPLETE!")
    print("=" * 80)
    print()
    print(f"📦 Package: {zip_filename}")
    print(f"📏 Size: {file_size:.2f} MB")
    print()
    print("📖 Next Steps:")
    print("   1. Extract the ZIP file")
    print("   2. Read START_HERE.md")
    print("   3. Follow RENDER_DEPLOYMENT.md for deployment")
    print("   4. Or run locally with: python run.py")
    print()
    print("🔑 Default License:")
    print("   Key: RENDER-2026-PROD-LIVE")
    print("   User: admin")
    print("   Pass: admin123")
    print()
    print("=" * 80)
    print("🎉 Ready for deployment! - جاهز للنشر!")
    print("=" * 80)

if __name__ == '__main__':
    create_complete_export()

