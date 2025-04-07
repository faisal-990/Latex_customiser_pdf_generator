#!/bin/bash

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "Python 3 not found. Please install Python 3.7+ first."
    exit 1
fi

# Install the package
pip install -e .

# Check for LaTeX
if ! command -v pdflatex &> /dev/null
then
    echo "pdflatex not found. Attempting to install LaTeX..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install texlive-latex-base texlive-latex-extra
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install --cask mactex
    else
        echo "Please install LaTeX manually: https://www.latex-project.org/get/"
    fi
fi

echo "Installation complete!"
echo "Run with: latex-selector"
