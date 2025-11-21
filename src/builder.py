import os
from pathlib import Path

def build_tex(selected):
    """Build LaTeX file with proper formatting and spacing."""
    # Use output directory relative to current working directory
    output_dir = Path.cwd() / "output"
    output_dir.mkdir(exist_ok=True)

    # Commands that should only appear once
    SINGLE_USE_COMMANDS = {
        'begin{document}', 'end{document}',
        'documentclass', 'usepackage'
    }

    preamble = """\\documentclass{article}
\\usepackage[table]{xcolor}
\\usepackage{amsmath}
\\begin{document}

"""
    with open(output_dir / "output.tex", "w") as f:
        f.write(preamble)
        
        if not selected:
            f.write("\\section{Default Section}\n\n")
            f.write("Sample content\n\n")
        else:
            prev_type = None
            for comp in selected:
                # Don't write duplicate document commands
                if any(cmd in comp.lower() for cmd in SINGLE_USE_COMMANDS):
                    continue
                
                # Determine component type for spacing
                current_type = get_component_type(comp)
                
                # Add spacing based on component type
                if current_type == 'section':
                    f.write("\n")  # Extra line before sections
                elif current_type == 'subsection':
                    f.write("\n")  # Line before subsections
                elif current_type in ['table', 'list', 'math']:
                    if prev_type in ['section', 'subsection']:
                        pass  # No extra space after headings
                    else:
                        f.write("\n")  # Space before environments
                
                # Write the component
                f.write(f"{comp}\n")
                
                # Add spacing after component
                if current_type in ['section', 'subsection']:
                    f.write("\n")  # Space after headings
                elif current_type in ['table', 'list', 'math']:
                    f.write("\n")  # Space after environments
                
                prev_type = current_type
        
        f.write("\n\\end{document}\n")


def get_component_type(comp):
    """Identify the type of LaTeX component."""
    comp_lower = comp.lower().strip()
    
    if comp_lower.startswith('\\section{'):
        return 'section'
    elif comp_lower.startswith('\\subsection{'):
        return 'subsection'
    elif comp_lower.startswith('\\subsubsection{'):
        return 'subsubsection'
    elif '\\begin{tabular}' in comp_lower:
        return 'table'
    elif '\\begin{itemize}' in comp_lower or '\\begin{enumerate}' in comp_lower:
        return 'list'
    elif comp_lower.startswith('\\[') or '$$' in comp_lower:
        return 'math'
    else:
        return 'other'

