import os
from pathlib import Path

def build_tex(selected):
    """Build LaTeX file while preventing duplicate document commands."""
    output_dir = Path("output")
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
            f.write("\\section{Default Section}\n")
            f.write("Sample content\\\\\n")
        else:
            for comp in selected:
                clean_comp = comp.strip('\\').strip()
                
                # Skip commands already in preamble
                if any(cmd in clean_comp.lower() for cmd in SINGLE_USE_COMMANDS):
                    continue
                    
                # Handle special cases
                if clean_comp.lower() == 'par':
                    f.write("\\\\\n")
                elif clean_comp:  # Only write non-empty commands
                    f.write(f"\\{clean_comp}\n")
        
        f.write("\\end{document}\n")
