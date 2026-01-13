#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile translation files (.po to .mo)
This script compiles all translation files for the application.
"""

import os
import sys
from babel.messages import mofile, pofile

def compile_translations():
    """Compile all .po files to .mo files"""
    
    translations_dir = 'translations'
    
    if not os.path.exists(translations_dir):
        print(f"❌ Error: {translations_dir} directory not found!")
        return False
    
    success_count = 0
    error_count = 0
    
    # Iterate through all language directories
    for lang_code in os.listdir(translations_dir):
        lang_dir = os.path.join(translations_dir, lang_code)
        
        if not os.path.isdir(lang_dir):
            continue
        
        lc_messages_dir = os.path.join(lang_dir, 'LC_MESSAGES')
        
        if not os.path.exists(lc_messages_dir):
            print(f"⚠️  Warning: LC_MESSAGES directory not found for {lang_code}")
            continue
        
        po_file = os.path.join(lc_messages_dir, 'messages.po')
        mo_file = os.path.join(lc_messages_dir, 'messages.mo')
        
        if not os.path.exists(po_file):
            print(f"⚠️  Warning: messages.po not found for {lang_code}")
            continue
        
        try:
            # Read .po file
            with open(po_file, 'rb') as f:
                catalog = pofile.read_po(f, locale=lang_code)
            
            # Write .mo file
            with open(mo_file, 'wb') as f:
                mofile.write_mo(f, catalog)
            
            print(f"✅ Compiled {lang_code}: {po_file} -> {mo_file}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error compiling {lang_code}: {str(e)}")
            error_count += 1
    
    print("\n" + "="*60)
    print(f"📊 Compilation Summary:")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Errors:  {error_count}")
    print("="*60)
    
    return error_count == 0

def extract_translations():
    """Extract translatable strings from source code"""
    print("\n🔍 Extracting translatable strings...")
    print("="*60)
    
    # Use pybabel to extract messages
    cmd = 'pybabel extract -F babel.cfg -o messages.pot .'
    
    print(f"Running: {cmd}")
    result = os.system(cmd)
    
    if result == 0:
        print("✅ Extraction successful!")
        return True
    else:
        print("❌ Extraction failed!")
        return False

def update_translations():
    """Update existing translation files with new strings"""
    print("\n🔄 Updating translation files...")
    print("="*60)
    
    translations_dir = 'translations'
    
    if not os.path.exists('messages.pot'):
        print("❌ Error: messages.pot not found! Run extract first.")
        return False
    
    for lang_code in os.listdir(translations_dir):
        lang_dir = os.path.join(translations_dir, lang_code)
        
        if not os.path.isdir(lang_dir):
            continue
        
        lc_messages_dir = os.path.join(lang_dir, 'LC_MESSAGES')
        po_file = os.path.join(lc_messages_dir, 'messages.po')
        
        if os.path.exists(po_file):
            cmd = f'pybabel update -i messages.pot -d {translations_dir} -l {lang_code}'
            print(f"Updating {lang_code}...")
            os.system(cmd)
    
    print("✅ Update complete!")
    return True

def main():
    """Main function"""
    print("\n" + "="*60)
    print("🌐 DED ERP Translation Compiler")
    print("="*60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'extract':
            extract_translations()
        elif command == 'update':
            update_translations()
        elif command == 'compile':
            compile_translations()
        elif command == 'all':
            if extract_translations():
                if update_translations():
                    compile_translations()
        else:
            print(f"❌ Unknown command: {command}")
            print("\nUsage:")
            print("  python compile_translations.py extract  - Extract strings")
            print("  python compile_translations.py update   - Update .po files")
            print("  python compile_translations.py compile  - Compile .po to .mo")
            print("  python compile_translations.py all      - Do all steps")
    else:
        # Default: just compile
        compile_translations()

if __name__ == '__main__':
    main()

