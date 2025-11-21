LaTeX Component Selector 📄✂️

A simple GUI tool to extract and reassemble parts of LaTeX documents. Select the sections, equations, tables, or lists you want and generate a new PDF with just those components.

✨ Features

    📂 Load any LaTeX .tex file
    🔍 Auto-detect sections, equations, tables, and lists
    ☑️ Pick and choose what to keep
    📝 Generate new LaTeX document
    🖨️ Compile to PDF instantly

🚀 Quick Start
Prerequisites

    Python 3.7+
    LaTeX (TeX Live, MacTeX, or MiKTeX)

Installation & Run
Linux / macOS
bash

# Clone the repository
git clone https://github.com/yourusername/latex-component-selector.git
cd latex-component-selector

# Run the installer (creates venv automatically)
chmod +x install.sh
./install.sh

# Launch the app
./run.sh

Windows
cmd

# Clone the repository
git clone https://github.com/yourusername/latex-component-selector.git
cd latex-component-selector

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install the package
pip install -e .

# Launch the app
run.bat

Or after first install, just run:
cmd

run.bat

Installing LaTeX (if needed)

Linux:
bash

sudo apt-get install texlive-latex-base texlive-latex-extra

macOS:
bash

brew install --cask mactex

Windows: Download and install MiKTeX
📖 Usage

    Launch: Run ./run.sh
    Load: Click "Load .tex files" and select your document
    Select: Check the components you want to keep
    Generate: Click "Generate PDF"
    View: PDF opens automatically, or click "View Output .tex" to see the LaTeX code

Example

Load this document:
latex

\section{Introduction}
Some intro text...

\section{Math}
\[ E = mc^2 \]

\section{Conclusion}
Final thoughts...

Select only "Introduction" and the equation → Get a new PDF with just those two parts!
🎯 What Gets Extracted

    Sections (\section, \subsection)
    Math equations (\[ ... \])
    Tables (\begin{tabular}...)
    Lists (itemize, enumerate)

🛠️ Troubleshooting

Problem: "pdflatex not found"
bash

sudo apt-get install texlive-latex-base texlive-latex-extra

Problem: Can't run scripts
bash

chmod +x install.sh run.sh

Problem: PDF won't open
bash

# Manually open the PDF
xdg-open output/output.pdf  # Linux
open output/output.pdf      # macOS

Check output/output.log for LaTeX compilation errors.
📁 Project Structure

├── src/              # Source code
├── install.sh        # One-click installer
├── run.sh            # Launch script
├── setup.py          # Package config
└── README.md         # This file

Generated files go in output/ (created automatically).
🤝 Contributing

Contributions welcome! Feel free to:

    Report bugs
    Suggest features
    Submit pull requests

📄 License

MIT License - see LICENSE file.
💡 Use Cases

    Extract specific sections for presentations
    Combine parts from multiple documents
    Create custom templates
    Study LaTeX structure
    Quick document cleanup

Made with ❤️ for the LaTeX community

For detailed technical documentation, see DEVELOPER_GUIDE.md.

