Here is the complete, reformed **README** file, integrating the clear, structured installation instructions separated by operating system.

-----

# LaTeX Component Selector 📄✂️

A simple **GUI tool** to extract and reassemble parts of LaTeX documents. Select the sections, equations, tables, or lists you want and generate a new PDF with just those components.

## ✨ Features

  * 📂 Load any LaTeX `.tex` file
  * 🔍 Auto-detect **sections, equations, tables, and lists**
  * ☑️ Pick and choose what to keep
  * 📝 Generate new LaTeX document
  * 🖨️ Compile to PDF instantly

-----

## 🚀 Quick Start: Installation & Run

This tool requires **Python 3.7+** and a working **LaTeX distribution** (TeX Live, MacTeX, or MiKTeX) installed on your system.

### Prerequisites (Install if needed)

| Operating System | LaTeX Distribution | Installation Command / Method |
| :--- | :--- | :--- |
| **Linux (Debian/Ubuntu)** | TeX Live | `sudo apt-get install texlive-latex-base texlive-latex-extra` |
| **macOS** | MacTeX | `brew install --cask mactex` (Requires Homebrew) |
| **Windows** | MiKTeX | **Download and install** from the [MiKTeX website](https://miktex.org/download) |

-----

### 💻 Installation & Execution

Follow the specific steps for your operating system below.

-----

### **🐧 macOS & Linux**

#### 1\. Clone the repository and navigate into the folder:

```bash
git clone https://github.com/yourusername/latex-component-selector.git
cd latex-component-selector
```

#### 2\. Install and Launch with the Scripts:

The **`install.sh`** script automatically sets up the virtual environment and installs dependencies.

```bash
# Make sure scripts are executable
chmod +x install.sh run.sh

# Run the installer (creates venv and installs dependencies)
./install.sh

# Launch the application
./run.sh
```

-----

### **🪟 Windows**

#### 1\. Clone the repository and navigate into the folder:

```cmd
git clone https://github.com/yourusername/latex-component-selector.git
cd latex-component-selector
```

#### 2\. Install and Launch with the Script:

The **`run.bat`** script handles environment activation, dependency installation, and launch the first time it's run.

```cmd
# Run the application (installs dependencies on first run)
run.bat
```

> **Tip:** For subsequent launches, just run `run.bat` again.

-----

## 📖 Usage

1.  **Launch:** Run the app using the command for your system (`./run.sh` or `run.bat`).
2.  **Load:** Click "**Load .tex files**" and select your LaTeX document.
3.  **Select:** Check the components (sections, equations, tables, lists) you want to keep in the output.
4.  **Generate:** Click "**Generate PDF**".
5.  **View:** The resulting PDF will open automatically, or you can click "**View Output .tex**" to see the generated LaTeX code.

### Example

Load this sample document:

```latex
\section{Introduction}
Some intro text...

\section{Math}
\[ E = mc^2 \]

\section{Conclusion}
Final thoughts...
```

Select only "**Introduction**" and the **equation** $\left( E = mc^2 \right)$ $\rightarrow$ Get a new PDF with just those two parts\!

### 🎯 What Gets Extracted

The tool intelligently parses the following LaTeX components:

  * **Sections:** (`\section`, `\subsection`, `\chapter`, etc.)
  * **Math equations:** (`\[ ... \]`, `$$...$$`, and `\begin{equation}...`)
  * **Tables:** (`\begin{tabular}`, `\begin{table}`, etc.)
  * **Lists:** (`\begin{itemize}`, `\begin{enumerate}`, etc.)

-----

## 🛠️ Troubleshooting

### **"pdflatex not found" Error**

This means your LaTeX distribution is not properly installed or configured in your system's PATH.

  * **Linux/macOS:** Ensure you have installed **TeX Live** or **MacTeX** correctly. For Linux, you might need to install additional packages:
    ```bash
    sudo apt-get install texlive-latex-base texlive-latex-extra
    ```

### **Can't run scripts (Linux/macOS)**

The scripts (`install.sh`, `run.sh`) need executable permissions.

```bash
chmod +x install.sh run.sh
```

### **PDF won't open**

The automatic PDF viewer may fail on some systems. You can manually open the generated file.

  * **Linux:** `xdg-open output/output.pdf`
  * **macOS:** `open output/output.pdf`

Check the `output/output.log` file for any LaTeX compilation errors.

-----

## 📁 Project Structure

```
├── src/              # Python Source code for the GUI logic
├── install.sh        # Linux/macOS One-click installer
├── run.sh            # Linux/macOS Launch script
├── run.bat           # Windows Launch script
├── setup.py          # Package configuration
└── README.md         # This file
```

> Generated output files (PDF, .tex, .log) are placed in the `output/` directory (created automatically).

-----

## 💡 Use Cases

  * Extract specific sections for **presentations** or handouts.
  * **Combine parts** from multiple documents into one new file.
  * Create **custom templates** from existing work.
  * Quickly **cleanup** or restructure a document.

-----

## 🤝 Contributing

We welcome contributions\! Feel free to:

  * Report bugs
  * Suggest features
  * Submit pull requests

-----

## 📄 License

**MIT License** - see the `LICENSE` file for details.

-----

Made with ❤️ for the LaTeX community
