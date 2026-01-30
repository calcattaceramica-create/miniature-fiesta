#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile translation files
"""

import os
from babel.messages import mofile, pofile

def compile_translations():
    """Compile all .po files to .mo files"""
    translations_dir = 'translations'
    
    for lang in ['ar', 'en']:
        po_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
        mo_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.mo')
        
        if os.path.exists(po_file):
            print(f"Compiling {po_file}...")
            with open(po_file, 'rb') as f:
                catalog = pofile.read_po(f)
            
            with open(mo_file, 'wb') as f:
                mofile.write_mo(f, catalog)
            
            print(f"✅ Compiled {mo_file}")
        else:
            print(f"❌ File not found: {po_file}")
    
    print("\n✅ All translations compiled successfully!")

if __name__ == '__main__':
    compile_translations()

