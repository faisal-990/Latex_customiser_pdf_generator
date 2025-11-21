import re


def extract_components(tex_content):
    """
    Extract LaTeX components while maintaining document structure.
    Groups content logically to keep sections with their subsections.
    Returns a list of tuples: (component_type, content, display_name)
    """
    components = []
    
    # Split into lines for position tracking
    lines = tex_content.split('\n')
    content = '\n'.join(lines)
    
    # Track positions of different components
    sections = []
    subsections = []
    tables = []
    lists = []
    math_blocks = []
    
    # Extract sections with positions
    for match in re.finditer(r'\\section\{([^}]+)\}', content):
        sections.append({
            'pos': match.start(),
            'cmd': 'section',
            'title': match.group(1),
            'full': match.group(0)
        })
    
    # Extract subsections with positions
    for match in re.finditer(r'\\subsection\{([^}]+)\}', content):
        subsections.append({
            'pos': match.start(),
            'cmd': 'subsection',
            'title': match.group(1),
            'full': match.group(0)
        })
    
    # Extract subsubsections with positions
    for match in re.finditer(r'\\subsubsection\{([^}]+)\}', content):
        subsections.append({
            'pos': match.start(),
            'cmd': 'subsubsection',
            'title': match.group(1),
            'full': match.group(0)
        })
    
    # Extract tables with positions
    for i, match in enumerate(re.finditer(r'\\begin\{tabular\}.*?\\end\{tabular\}', content, re.DOTALL), 1):
        tables.append({
            'pos': match.start(),
            'content': match.group(0),
            'name': f'[Table {i}]'
        })
    
    # Extract itemize lists
    for i, match in enumerate(re.finditer(r'\\begin\{itemize\}.*?\\end\{itemize\}', content, re.DOTALL), 1):
        lists.append({
            'pos': match.start(),
            'content': match.group(0),
            'name': f'[Bullet List {i}]'
        })
    
    # Extract enumerate lists
    enum_start = len(lists) + 1
    for i, match in enumerate(re.finditer(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', content, re.DOTALL), enum_start):
        lists.append({
            'pos': match.start(),
            'content': match.group(0),
            'name': f'[Numbered List {i}]'
        })
    
    # Extract display math
    for i, match in enumerate(re.finditer(r'\\\[.*?\\\]', content, re.DOTALL), 1):
        math_content = match.group(0)
        preview = math_content[:60].replace('\n', ' ').strip()
        if len(math_content) > 60:
            preview += '...'
        math_blocks.append({
            'pos': match.start(),
            'content': math_content,
            'name': f'[Equation {i}] {preview}'
        })
    
    # Combine all components with their positions
    all_items = []
    
    for sec in sections:
        all_items.append({
            'pos': sec['pos'],
            'type': 'section',
            'content': sec['full'],
            'display': sec['full']
        })
    
    for subsec in subsections:
        all_items.append({
            'pos': subsec['pos'],
            'type': 'subsection',
            'content': subsec['full'],
            'display': subsec['full']
        })
    
    for table in tables:
        all_items.append({
            'pos': table['pos'],
            'type': 'table',
            'content': table['content'],
            'display': table['name']
        })
    
    for lst in lists:
        all_items.append({
            'pos': lst['pos'],
            'type': 'list',
            'content': lst['content'],
            'display': lst['name']
        })
    
    for math in math_blocks:
        all_items.append({
            'pos': math['pos'],
            'type': 'math',
            'content': math['content'],
            'display': math['name']
        })
    
    # Sort by position to maintain document order
    all_items.sort(key=lambda x: x['pos'])
    
    # Convert to return format
    for item in all_items:
        components.append((item['type'], item['content'], item['display']))
    
    return components

