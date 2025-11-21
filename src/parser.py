import re


def extract_components(tex_content):
    """
    Extract meaningful LaTeX components from a document.
    Returns a list of tuples: (component_type, content, display_name)
    """
    components = []
    
    # Extract sections and subsections
    section_pattern = r'\\(section|subsection|subsubsection)\{([^}]+)\}'
    for match in re.finditer(section_pattern, tex_content):
        cmd, title = match.groups()
        components.append((f'{cmd}', f'{{{title}}}', f'\\{cmd}{{{title}}}'))
    
    # Extract complete table environments
    table_pattern = r'(\\begin\{tabular\}.*?\\end\{tabular\})'
    for i, match in enumerate(re.finditer(table_pattern, tex_content, re.DOTALL), 1):
        table_content = match.group(1)
        # Create a shortened display name
        lines = table_content.split('\n')
        preview = lines[0][:50] + '...' if len(lines[0]) > 50 else lines[0]
        components.append(('tabular', table_content, f'[Table {i}] {preview}'))
    
    # Extract itemize environments
    itemize_pattern = r'(\\begin\{itemize\}.*?\\end\{itemize\})'
    for i, match in enumerate(re.finditer(itemize_pattern, tex_content, re.DOTALL), 1):
        content = match.group(1)
        components.append(('itemize', content, f'[Bullet List {i}]'))
    
    # Extract enumerate environments
    enumerate_pattern = r'(\\begin\{enumerate\}.*?\\end\{enumerate\})'
    for i, match in enumerate(re.finditer(enumerate_pattern, tex_content, re.DOTALL), 1):
        content = match.group(1)
        components.append(('enumerate', content, f'[Numbered List {i}]'))
    
    # Extract math environments (display math)
    math_pattern = r'(\\\[.*?\\\])'
    for i, match in enumerate(re.finditer(math_pattern, tex_content, re.DOTALL), 1):
        content = match.group(1)
        preview = content[:50].replace('\n', ' ')
        components.append(('math', content, f'[Math {i}] {preview}...'))
    
    return components
