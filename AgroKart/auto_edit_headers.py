#!/usr/bin/env python3
"""
Auto-Edit Script for AgroKart Headers
This script automatically updates all HTML templates to use consistent headers
"""

import os
import re
from pathlib import Path

def find_html_files(directory):
    """Find all HTML files in the templates directory"""
    html_files = []
    templates_dir = Path(directory) / "core" / "templates" / "core"
    
    if templates_dir.exists():
        for file in templates_dir.glob("*.html"):
            if file.name not in ['base_header.html']:  # Skip the base header file
                html_files.append(file)
    
    return html_files

def extract_header_section(content):
    """Extract the header section from HTML content"""
    # Pattern to match header tag and its content
    header_pattern = r'<header[^>]*>.*?</header>'
    header_match = re.search(header_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if header_match:
        return header_match.group(0), header_match.start(), header_match.end()
    
    return None, None, None

def extract_header_styles(content):
    """Extract header-related CSS styles"""
    # Find style tag content
    style_pattern = r'<style[^>]*>(.*?)</style>'
    style_match = re.search(style_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not style_match:
        return None, None, None
    
    style_content = style_match.group(1)
    
    # Header-related CSS patterns
    header_css_patterns = [
        r'header\s*{[^}]*}',
        r'\.logo[^{]*{[^}]*}',
        r'nav[^{]*{[^}]*}',
        r'\.avatar[^{]*{[^}]*}',
        r'\.dropdown[^{]*{[^}]*}',
        r'\.lang-toggle[^{]*{[^}]*}',
        r'\.avatar-container[^{]*{[^}]*}',
        r'\.nav-avatar[^{]*{[^}]*}',
    ]
    
    # Find and remove header-related CSS
    cleaned_style = style_content
    for pattern in header_css_patterns:
        cleaned_style = re.sub(pattern, '', cleaned_style, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up extra whitespace
    cleaned_style = re.sub(r'\n\s*\n', '\n', cleaned_style)
    cleaned_style = cleaned_style.strip()
    
    return style_content, cleaned_style, (style_match.start(1), style_match.end(1))

def update_html_file(file_path):
    """Update a single HTML file with the new header"""
    print(f"Processing: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already includes base_header
        if '{% include "core/base_header.html" %}' in content:
            print(f"  ✓ {file_path.name} already uses base_header.html")
            return True
        
        # Extract and remove old header
        old_header, header_start, header_end = extract_header_section(content)
        if old_header:
            content = content[:header_start] + content[header_end:]
            print(f"  - Removed old header from {file_path.name}")
        
        # Extract and clean header-related CSS
        original_style, cleaned_style, style_positions = extract_header_styles(content)
        if original_style and style_positions:
            start_pos, end_pos = style_positions
            # Find the full style tag
            style_tag_start = content.rfind('<style', 0, start_pos)
            style_tag_end = content.find('</style>', end_pos) + 8
            
            if cleaned_style.strip():
                # Keep non-header styles
                new_style_content = f"<style>\n{cleaned_style}\n  </style>"
                content = content[:style_tag_start] + new_style_content + content[style_tag_end:]
            else:
                # Remove entire style tag if only header styles
                content = content[:style_tag_start] + content[style_tag_end:]
            
            print(f"  - Cleaned header CSS from {file_path.name}")
        
        # Add the include directive after {% load static %}
        if '{% load static %}' in content:
            content = content.replace(
                '{% load static %}',
                '{% load static %}\n{% include "core/base_header.html" %}'
            )
        else:
            # Add at the beginning of body tag
            body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n{% include "core/base_header.html" %}\n' + content[insert_pos:]
        
        # Ensure body has proper padding-top for fixed header
        if '<body' in content and 'padding-top' not in content:
            # Add padding-top to body if not present
            body_pattern = r'(<body[^>]*>)'
            body_replacement = r'\1\n<style>body { padding-top: 70px; }</style>'
            content = re.sub(body_pattern, body_replacement, content, flags=re.IGNORECASE)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Updated {file_path.name} successfully")
        return True
        
    except Exception as e:
        print(f"  ✗ Error updating {file_path.name}: {str(e)}")
        return False

def main():
    """Main function to run the auto-edit process"""
    print("🚀 AgroKart Header Auto-Edit Script")
    print("=" * 50)
    
    # Get the project directory
    project_dir = Path(__file__).parent
    print(f"Project directory: {project_dir}")
    
    # Find all HTML files
    html_files = find_html_files(project_dir)
    
    if not html_files:
        print("❌ No HTML files found in core/templates/core/")
        return
    
    print(f"📁 Found {len(html_files)} HTML files to process")
    print()
    
    # Process each file
    success_count = 0
    for file_path in html_files:
        if update_html_file(file_path):
            success_count += 1
        print()
    
    # Summary
    print("=" * 50)
    print(f"✅ Successfully updated {success_count}/{len(html_files)} files")
    
    if success_count == len(html_files):
        print("🎉 All files updated successfully!")
        print("\n📋 Next steps:")
        print("1. Test your pages to ensure they work correctly")
        print("2. Check that the header appears consistently across all pages")
        print("3. Verify that language toggle and dropdown work properly")
    else:
        print("⚠️  Some files had issues. Please check the output above.")

if __name__ == "__main__":
    main()