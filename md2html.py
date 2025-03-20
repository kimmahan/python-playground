#!/usr/bin/env python3
"""
Markdown to HTML Converter

A simple command-line tool to convert Markdown files to HTML.
Usage: python md2html.py <input_file.md> [output_file.html]
If no output file is specified, it will use the same name as the input file with .html extension.
"""

import sys
import re
import os
from pathlib import Path

def convert_markdown_to_html(markdown_text):
    """Convert markdown text to HTML."""
    html = markdown_text
    
    # Convert headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
    
    # Convert bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Convert links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Convert code blocks
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Convert unordered lists
    # First, find all list blocks
    list_pattern = re.compile(r'((?:^- .*?\n)+)', re.MULTILINE)
    list_matches = list_pattern.finditer(html)
    
    for match in reversed(list(list_matches)):
        list_text = match.group(1)
        list_items = re.findall(r'^- (.*?)$', list_text, re.MULTILINE)
        list_html = "<ul>\n" + "\n".join([f"  <li>{item}</li>" for item in list_items]) + "\n</ul>"
        html = html[:match.start()] + list_html + html[match.end():]
    
    # Convert ordered lists
    list_pattern = re.compile(r'((?:^\d+\. .*?\n)+)', re.MULTILINE)
    list_matches = list_pattern.finditer(html)
    
    for match in reversed(list(list_matches)):
        list_text = match.group(1)
        list_items = re.findall(r'^\d+\. (.*?)$', list_text, re.MULTILINE)
        list_html = "<ol>\n" + "\n".join([f"  <li>{item}</li>" for item in list_items]) + "\n</ol>"
        html = html[:match.start()] + list_html + html[match.end():]
    
    # Convert paragraphs (any line that's not already converted)
    # First, collapse consecutive lines that aren't headers, lists, or code blocks
    paragraph_pattern = re.compile(r'(?<!\n\n)(?<!<h\d>)(?<!<\/h\d>)(?<!<ul>)(?<!<\/ul>)(?<!<ol>)(?<!<\/ol>)(?<!<pre>)(?<!<\/pre>)(?<!<p>)(?<!<\/p>)^([^<].*?)$(?!\n\n)(?!<h\d>)(?!<\/h\d>)(?!<ul>)(?!<\/ul>)(?!<ol>)(?!<\/ol>)(?!<pre>)(?!<\/pre>)(?!<p>)(?!<\/p>)', re.MULTILINE)
    html = paragraph_pattern.sub(r'<p>\1</p>', html)
    
    # Add horizontal rules
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)
    
    return html

def create_html_document(html_body, title="Converted Markdown"):
    """Wrap the converted HTML in a complete HTML document."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0 auto; max-width: 800px; padding: 20px; }}
        pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        code {{ background-color: #f5f5f5; padding: 2px 4px; border-radius: 3px; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python md2html.py <input_file.md> [output_file.html]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Use the same name but with .html extension
        input_path = Path(input_file)
        output_file = input_path.with_suffix('.html')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        html_body = convert_markdown_to_html(markdown_content)
        html_document = create_html_document(html_body, title=os.path.basename(input_file))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_document)
        
        print(f"Conversion successful: {input_file} → {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()