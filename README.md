LaTeX Component Selector 📄✂️

A PyQt5-based GUI application that lets you extract, select, and reassemble components from LaTeX documents. Perfect for creating customized documents by cherry-picking sections, equations, tables, and lists from existing LaTeX files.

🎯 Features

    📂 Load LaTeX Files - Import any .tex document
    🔍 Smart Extraction - Automatically detects:
        Sections and subsections
        Mathematical equations
        Tables
        Itemized and numbered lists
    ☑️ Component Selection - Check/uncheck components you want
    📝 Generate Custom Documents - Creates new LaTeX file with only selected components
    🖨️ Instant PDF Generation - Compiles to PDF automatically
    👀 Preview Support - View generated .tex file before compilation

🖼️ Screenshots

┌─────────────────────────────────────────┐
│  LaTeX Component Selector               │
├─────────────────────────────────────────┤
│  Select components                      │
│  ┌───────────────────────────────────┐  │
│  │ ☑ \section{Introduction}          │  │
│  │ ☑ \subsection{Purpose}            │  │
│  │ ☐ \subsection{Scope}              │  │
│  │ ☑ [Equation 1] \[ x = \frac...    │  │
│  │ ☐ [Table 1] \begin{tabular}...    │  │
│  │ ☑ [Bullet List 1]                 │  │
│  └───────────────────────────────────┘  │
│  [Load .tex files]                      │
│  [Generate PDF] [View Output .tex]      │
└─────────────────────────────────────────┘

🚀 Quick Start
Prerequisites

    Python 3.7+
    LaTeX distribution (TeX Live on Linux, MacTeX on macOS, MiKTeX on Windows)

Installation
Option 1: Automated Installation (Linux/macOS)
bash

# Clone the repository
git clone https://github.com/yourusername/latex-component-selector.git
cd latex-component-selector

# Run installer
chmod +x install.sh
./install.sh

# Run the application
./run.sh

Option 2: Manual Installation
bash

# Clone the repository
git clone https://github.com/yourusername/latex-component-selector.git
cd latex-component-selector

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the application
latex-selector

Installing LaTeX (if not already installed)

Ubuntu/Debian:
bash

sudo apt-get update
sudo apt-get install texlive-latex-base texlive-latex-extra

macOS:
bash

brew install --cask mactex

Windows:

    Download and install MiKTeX

📖 Usage
Basic Workflow

    Launch the application

bash

   ./run.sh  # or: latex-selector

    Load a LaTeX file
        Click "Load .tex files"
        Select your .tex document
        Components will be extracted and displayed
    Select components
        Check the boxes next to components you want to keep
        Components appear in document order
    Generate PDF
        Click "Generate PDF"
        The application will:
            Create output/output.tex with selected components
            Compile to output/output.pdf
            Open the PDF automatically
    View LaTeX source (optional)
        Click "View Output .tex" to see the generated LaTeX code

Example

Input file (demo.tex):
latex

\section{Introduction}
Introduction text here...

\section{Math}
\[ E = mc^2 \]

\section{Conclusion}
Conclusion text here...

After selecting only "Introduction" and the equation:

Output (output.tex):
latex

\documentclass{article}
\usepackage[table]{xcolor}
\usepackage{amsmath}
\begin{document}

\section{Introduction}

\[ E = mc^2 \]

\end{document}

🎓 Use Cases

    Academic Papers - Extract specific sections for presentations
    Report Generation - Combine sections from multiple documents
    Template Creation - Build custom templates from existing documents
    Learning LaTeX - Study how different components are structured
    Document Cleanup - Remove unwanted sections while preserving formatting

🗂️ Project Structure

latex-component-selector/
├── src/
│   ├── main.py          # Application entry point
│   ├── gui.py           # PyQt5 interface
│   ├── parser.py        # LaTeX component extraction
│   ├── builder.py       # LaTeX file assembly
│   ├── compiler.py      # PDF compilation
│   └── data/            # Sample .tex files
├── output/              # Generated files (created automatically)
│   ├── output.tex       # Generated LaTeX
│   └── output.pdf       # Compiled PDF
├── install.sh           # Automated installer
├── run.sh               # Convenience script
├── setup.py             # Package configuration
└── README.md            # This file

⚙️ Configuration
Supported Component Types

Currently extracts:

    \section{...}
    \subsection{...}
    \subsubsection{...}
    \begin{tabular}...\end{tabular} (complete tables)
    \begin{itemize}...\end{itemize} (bullet lists)
    \begin{enumerate}...\end{enumerate} (numbered lists)
    \[ ... \] (display math equations)

Custom LaTeX Packages

The default preamble includes:
latex

\usepackage[table]{xcolor}  % For colored tables
\usepackage{amsmath}        % For mathematical equations

To add more packages, modify src/builder.py:
python

preamble = """\\documentclass{article}
\\usepackage[table]{xcolor}
\\usepackage{amsmath}
\\usepackage{graphicx}  # Add your package here
\\begin{document}
"""

🛠️ Troubleshooting
Common Issues

Problem: "Module not found: src"
bash

# Solution: Activate virtual environment
source venv/bin/activate
pip install -e .

Problem: "pdflatex: command not found"
bash

# Solution: Install LaTeX
# Ubuntu/Debian:
sudo apt-get install texlive-latex-base texlive-latex-extra

Problem: "Package array Error: Illegal pream-token"

    This occurs if you manually select table formatting commands
    Solution: Select complete [Table N] items instead of individual commands

Problem: PDF not opening automatically
bash

# Install a PDF viewer
# Linux:
sudo apt-get install zathura  # or evince, okular

# Then manually open:
zathura output/output.pdf

Debug Mode

To see detailed LaTeX compilation output:
bash

# Run from terminal to see compilation logs
latex-selector

Check output/output.log for LaTeX errors.
🤝 Contributing

Contributions are welcome! Here's how you can help:

    Fork the repository
    Create a feature branch (git checkout -b feature/AmazingFeature)
    Commit your changes (git commit -m 'Add some AmazingFeature')
    Push to the branch (git push origin feature/AmazingFeature)
    Open a Pull Request

Ideas for Contributions

    Add support for figures and images
    Implement drag-and-drop component reordering
    Add live LaTeX preview panel
    Support for BibTeX references
    Export to other formats (Markdown, HTML)
    Dark mode theme
    Component search/filter functionality

📋 Requirements

    Python 3.7 or higher
    PyQt5 >= 5.15.7
    LaTeX distribution (TeX Live, MacTeX, or MiKTeX)
    Operating System: Linux, macOS, or Windows

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

    Built with PyQt5
    LaTeX compilation via pdflatex
    Inspired by the need for modular LaTeX document management

📧 Contact

Project Maintainer: Sawez
Issues: https://github.com/yourusername/latex-component-selector/issues
Discussions: https://github.com/yourusername/latex-component-selector/discussions
🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

Made with ❤️ for the LaTeX community

