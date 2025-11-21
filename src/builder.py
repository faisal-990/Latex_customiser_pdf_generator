import os
from pathlib import Path

def build_tex(selected):
    """Build LaTeX file while preventing duplicate document commands."""
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
            f.write("\\section{Default Section}\n")
            f.write("Sample content\\\\\n")
        else:
            for comp in selected:
                # Don't strip or modify - write content as-is
                if not any(cmd in comp.lower() for cmd in SINGLE_USE_COMMANDS):
                    f.write(f"{comp}\n")
        
        f.write("\\end{document}\n")
