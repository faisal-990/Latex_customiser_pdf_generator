#!/bin/bash

set -e  # Exit on any error

echo "======================================"
echo "LaTeX Component Selector - Installer"
echo "======================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 not found. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install the package
echo ""
echo "📥 Installing latex-selector..."
pip install -e .

echo ""
echo "✅ Package installed successfully!"

# Check for LaTeX
echo ""
echo "🔍 Checking for LaTeX installation..."
if ! command -v pdflatex &> /dev/null
then
    echo "⚠️  pdflatex not found. Attempting to install LaTeX..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installing LaTeX on Linux..."
        sudo apt-get update
        sudo apt-get install -y texlive-latex-base texlive-latex-extra
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing LaTeX on macOS..."
        brew install --cask mactex
    else
        echo "❌ Please install LaTeX manually: https://www.latex-project.org/get/"
    fi
else
    echo "✅ LaTeX found: $(pdflatex --version | head -n 1)"
fi

echo ""
echo "======================================"
echo "✅ Installation complete!"
echo "======================================"
echo ""
echo "To use the application:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     latex-selector"
echo ""
echo "  3. To deactivate when done:"
echo "     deactivate"
echo ""
echo "Or use the run script:"
echo "  ./run.sh"
echo "======================================"
