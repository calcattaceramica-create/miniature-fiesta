#!/usr/bin/env python3
"""
Script to apply responsive design patterns to all HTML templates
"""

import os
import re
from pathlib import Path

# Define the templates directory
TEMPLATES_DIR = Path("app/templates")

# Patterns to replace
PATTERNS = {
    # Page Header Pattern
    'page_header_old': r'<div class="page-header d-flex justify-content-between align-items-center">',
    'page_header_new': '''<div class="container-fluid">
    <div class="page-header mb-4">
        <div class="d-flex justify-content-between align-items-center flex-wrap">''',
    
    # Close page header
    'page_header_close_old': r'</div>\s*</div>\s*<!-- (Filters|Search|Table)',
    'page_header_close_new': '''        </div>
    </div>

    <!-- \\1''',
    
    # Row with columns
    'row_old': r'<div class="row">',
    'row_new': '<div class="row g-2">',
    
    # Column responsive
    'col_md_6': r'<div class="col-md-6">',
    'col_12_md_6': '<div class="col-12 col-md-6">',
    
    'col_md_4': r'<div class="col-md-4">',
    'col_12_md_4': '<div class="col-12 col-md-4">',
    
    'col_md_3': r'<div class="col-md-3">',
    'col_12_md_3': '<div class="col-12 col-md-3">',
    
    'col_lg_6': r'<div class="col-md-6">',
    'col_12_lg_6': '<div class="col-12 col-lg-6">',
    
    # Table headers - add hide-on-mobile to less important columns
    'th_category': r'<th>{{ _\(\'Category\'\) }}</th>',
    'th_category_hide': '<th class="hide-on-mobile">{{ _(\'Category\') }}</th>',
    
    'th_unit': r'<th>{{ _\(\'Unit\'\) }}</th>',
    'th_unit_hide': '<th class="hide-on-mobile">{{ _(\'Unit\') }}</th>',
    
    'th_date': r'<th>{{ _\(\'Date\'\) }}</th>',
    'th_date_hide': '<th class="hide-on-mobile">{{ _(\'Date\') }}</th>',
    
    # Buttons - hide text on mobile
    'btn_text': r'<i class="([^"]+)"></i> {{ _\(\'([^\']+)\'\) }}',
    'btn_text_responsive': r'<i class="\1"></i> <span class="d-none d-sm-inline">{{ _(\'\2\') }}</span>',
    
    # Card spacing
    'card_mt_3': r'<div class="card mt-3">',
    'card_mb_3': '<div class="card mb-3">',
    
    # Pagination
    'pagination_ul': r'<ul class="pagination justify-content-center">',
    'pagination_ul_wrap': '<ul class="pagination justify-content-center flex-wrap">',
}

def apply_responsive_to_file(file_path):
    """Apply responsive design patterns to a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Apply each pattern
        for pattern_name, pattern in PATTERNS.items():
            if pattern_name.endswith('_old') or pattern_name.endswith('_new'):
                continue
            
            # Get the old and new patterns
            old_key = pattern_name
            new_key = pattern_name.replace('_old', '_new')
            
            if old_key in PATTERNS and new_key in PATTERNS:
                old_pattern = PATTERNS[old_key]
                new_pattern = PATTERNS[new_key]
                
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    changes_made.append(pattern_name)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        
        return False, []
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, []

def process_directory(directory):
    """Process all HTML files in a directory"""
    html_files = list(directory.rglob("*.html"))
    
    print(f"Found {len(html_files)} HTML files")
    print("=" * 60)
    
    total_modified = 0
    
    for html_file in html_files:
        # Skip base.html as it's already updated
        if html_file.name == 'base.html':
            continue
        
        modified, changes = apply_responsive_to_file(html_file)
        
        if modified:
            total_modified += 1
            print(f"✅ Modified: {html_file.relative_to(TEMPLATES_DIR)}")
            if changes:
                print(f"   Changes: {', '.join(changes[:3])}...")
        else:
            print(f"⏭️  Skipped: {html_file.relative_to(TEMPLATES_DIR)}")
    
    print("=" * 60)
    print(f"Total files modified: {total_modified}/{len(html_files)}")

def main():
    """Main function"""
    print("🎨 Applying Responsive Design to All Templates")
    print("=" * 60)
    
    if not TEMPLATES_DIR.exists():
        print(f"❌ Templates directory not found: {TEMPLATES_DIR}")
        return
    
    # Process all subdirectories
    subdirs = [
        'inventory',
        'sales',
        'purchases',
        'accounting',
        'hr',
        'pos',
        'reports',
        'settings',
        'crm',
    ]
    
    for subdir in subdirs:
        subdir_path = TEMPLATES_DIR / subdir
        if subdir_path.exists():
            print(f"\n📁 Processing: {subdir}")
            print("-" * 60)
            process_directory(subdir_path)
    
    print("\n✅ Responsive design application complete!")

if __name__ == "__main__":
    main()

