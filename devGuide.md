

````markdown
# LaTeX Component Selector - Developer Guide

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Architecture & Flow](#-architecture--flow)
3. [Component Breakdown](#-component-breakdown)
4. [Dependencies](#-dependencies)
5. [Data Flow](#-data-flow)
6. [Code Walkthrough](#-code-walkthrough)
7. [Common Issues & Solutions](#-common-issues--solutions)
8. [Development Tips](#-development-tips)
9. [Further Reading](#-further-reading)

---

## 🎯 Project Overview

**LaTeX Component Selector** is a PyQt5-based GUI application that allows users to:
* Load a LaTeX (`.tex`) file.
* Extract and display individual components (sections, tables, equations, lists).
* Select which components to keep.
* Generate a new LaTeX file and PDF with only the selected components.

**Use Case:** Useful for creating customized documents from existing LaTeX files, cherry-picking specific sections, tables, or equations without manual editing.

---

## 🏗️ Architecture & Flow

The application follows a linear flow from user interaction to PDF generation.

```text
┌─────────────┐
│   User      │
│  Clicks     │
│ "Load .tex" │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                     gui.py (Main Interface)                 │
│  - QWidget with buttons and list display                    │
│  - Handles user interactions                                │
└──────┬──────────────────────────────────────┬───────────────┘
       │                                      │
       │ Reads file                           │ User selects
       ▼                                      │ components
┌─────────────────┐                           │
│   parser.py     │                           │
│  - Regex-based  │                           │
│  - Extracts:    │                           │
│    • Sections   │                           │
│    • Tables     │                           │
│    • Math       │                           │
│    • Lists      │                           │
└────────┬────────┘                           │
         │                                    │
         │ Returns list of                    │
         │ (type, content, display_name)      │
         ▼                                    │
┌─────────────────────────────────────────┐   │
│         Display in QListWidget          │   │
│       (with checkboxes)                 │   │
└─────────────────────────────────────────┘   │
                                              │
       User clicks "Generate PDF"             │
                    │                         │
                    ▼                         │
         ┌──────────────────┐                 │
         │   builder.py     │◄────────────────┘
         │  - Assembles     │  Selected components
         │    LaTeX file    │
         │  - Adds preamble │
         │  - Formats       │
         └────────┬─────────┘
                  │
                  │ Writes output.tex
                  ▼
         ┌──────────────────┐
         │  compiler.py     │
         │  - Runs pdflatex │
         │  - Generates PDF │
         └────────┬─────────┘
                  │
                  │ Creates output.pdf
                  ▼
         ┌──────────────────┐
         │  Opens PDF in    │
         │  system viewer   │
         └──────────────────┘
````

-----

## 🧩 Component Breakdown

### 1\. main.py - Entry Point

**Purpose:** Application bootstrap.

**What it does:**

  * Creates `QApplication` instance.
  * Instantiates `ComponentSelector` window.
  * Sets up signal handling (Ctrl+C).
  * Starts event loop.

**Key Code:**

```python
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Handle Ctrl+C gracefully
    app = QApplication(sys.argv)
    window = ComponentSelector()
    window.show()
    sys.exit(app.exec_())
```

### 2\. gui.py - User Interface

**Purpose:** PyQt5-based graphical interface.

**Components:**

  * `QListWidget`: Displays extractable components with checkboxes.
  * `QPushButton`: Load file, Generate PDF, View .tex buttons.
  * `QLabel`: Status/instruction text.

**Key Methods:**

**`load_tex_file()`**

1.  Opens `QFileDialog` to select .tex file.
2.  Reads file content.
3.  Calls `parser.extract_components()`.
4.  Populates `QListWidget` with results.
5.  Stores actual LaTeX content in `Qt.UserRole` (hidden data).

**`generate_tex_file()`**

1.  Iterates through list items.
2.  Collects checked items' content (from `Qt.UserRole`).
3.  Calls `builder.build_tex()` with selected content.
4.  Calls `compiler.compile_pdf()`.
5.  Opens resulting PDF.

> **Why Qt.UserRole?**
>
>   * **Display name:** Shows user-friendly text (e.g., `[Table 1] \begin{tabular}...`).
>   * **Qt.UserRole:** Stores the actual raw LaTeX code required for reconstruction.

### 3\. parser.py - Component Extraction

**Purpose:** Parse LaTeX file and extract meaningful components.

**How it works:**

**Step 1: Pattern Matching with Regex**

```python
# Extract sections
r'\\section\{([^}]+)\}'  # Matches: \section{Title}

# Extract tables
r'\\begin\{tabular\}.*?\\end\{tabular\}'  # Matches entire table block

# Extract math
r'\\\[.*?\\\]'  # Matches: \[ equation \]
```

**Step 2: Position Tracking**

```python
for match in re.finditer(pattern, content):
    items.append({
        'pos': match.start(),  # Character position in file
        'content': match.group(0),
        'display': formatted_name
    })
```

**Step 3: Sorting by Position**

```python
all_items.sort(key=lambda x: x['pos'])
```

*Why?* Maintains document order so components appear in the list exactly as they do in the original file.

**Return Format:**

```python
[
    ('section', '\\section{Introduction}', '\\section{Introduction}'),
    ('math', '\\[ x = ... \\]', '[Equation 1] \\[ x = ...'),
    ('table', '\\begin{tabular}...\\end{tabular}', '[Table 1] ...')
]
# Structure: (type, actual_content, display_name)
```

### 4\. builder.py - LaTeX File Assembly

**Purpose:** Construct valid LaTeX document from selected components.

**Process:**

1.  **Create Document Structure:**

    ```python
    preamble = """
    \\documentclass{article}
    \\usepackage[table]{xcolor}  # For colored tables
    \\usepackage{amsmath}        # For math equations
    \\begin{document}
    """
    ```

2.  **Smart Formatting:**

      * Identifies component types (`section`, `table`, `math`, etc.).
      * Adds appropriate spacing (extra lines before sections, space after headings).

3.  **Write Components:**

      * Skips duplicate preamble commands.
      * Writes component content as-is.

4.  **Close Document:**

      * Writes `\end{document}`.
      * **Output Location:** `output/output.tex`.

### 5\. compiler.py - PDF Generation

**Purpose:** Compile LaTeX to PDF using `pdflatex`.

**Process:**

1.  **Locate Files:**

    ```python
    output_dir = Path.cwd() / "output"
    tex_file = output_dir / "output.tex"
    ```

2.  **Run pdflatex:**

    ```python
    subprocess.run([
        "pdflatex",
        "-interaction=nonstopmode",  # Don't stop on errors
        "-halt-on-error",             # But halt on fatal errors
        f"-output-directory={output_dir}",
        str(tex_file.name)
    ], cwd=str(output_dir), ...)
    ```

    *Why run from `output_dir`?* `pdflatex` generates auxiliary files (.aux, .log). This keeps the project root clean.

3.  **Verify Success:**
    Checks if `output.pdf` exists. Includes a 30-second timeout to prevent hangs.

-----

## 📦 Dependencies

### PyQt5 (v5.15.7+)

  * **Why?** Cross-platform GUI framework.
  * **Components Used:** `QApplication`, `QWidget`, `QListWidget`, `QListWidgetItem`, `QPushButton`, `QFileDialog`, `QMessageBox`, `QVBoxLayout`/`QHBoxLayout`.
  * **Alternative Considered:** Tkinter (built-in but less modern/flexible).

### System Dependencies

  * **pdflatex (TeX Live)**
      * **Why?** Compiles .tex → .pdf.
      * **Packages Needed:** `texlive-latex-base` (Core), `texlive-latex-extra` (xcolor, amsmath).
      * **Call command:** `pdflatex -interaction=nonstopmode output.tex`

### Python Standard Library

  * **re:** Pattern matching (`re.DOTALL` used for multi-line blocks).
  * **subprocess:** Execute external programs (`pdflatex`).
  * **pathlib:** Cross-platform path handling (`Path.cwd()`).
  * **sys:** Application exit codes.
  * **signal:** Handle Ctrl+C gracefully.

-----

## 🔄 Data Flow

**Complete User Journey**

1.  **User Action:** Load `demo.tex`.
2.  **gui.py:** Reads file content.
3.  **parser.py:** Receives raw LaTeX string.
4.  **Regex:** Patterns extract components with positions.
5.  **Sort:** Components sorted by position (document order).
6.  **Return:** `[('section', '\\section{Intro}', '\\section{Intro}'), ...]`
7.  **gui.py:** Creates `QListWidgetItem` for each.
8.  **Display:** "✓ \\section{Introduction}"
9.  **User Action:** Checks/Unchecks items → Clicks "Generate PDF".
10. **gui.py:** Collects checked items' `Qt.UserRole` data.
11. **builder.py:** Receives `['\\section{Intro}', '\\[ x = ... \\]']`.
12. **Write:** Formats LaTeX to `output/output.tex`.
13. **compiler.py:** Runs `pdflatex output.tex`.
14. **Generate:** Creates `output/output.pdf`.
15. **View:** Opens PDF in system viewer.

-----

## 💻 Code Walkthrough

### Example: Loading a File

**User clicks "Load .tex files"**

**`gui.py - load_tex_file()`**

```python
def load_tex_file(self):
    # 1. Open file dialog
    file_path, _ = QFileDialog.getOpenFileName(
        self, "Open .tex files", "", "TeX files (*.tex)"
    )
    if not file_path:
        return  # User cancelled
    
    # 2. Read file
    with open(file_path, "r") as f:
        content = f.read()
        
        # 3. Extract components
        components = extract_components(content)
        
        # 4. Clear existing list
        self.list_widget.clear()
        
        # 5. Populate list
        for comp in components:
            # comp = ('section', '\\section{Title}', '\\section{Title}')
            _, content, display_name = comp
            
            # Create list item
            item = QListWidgetItem(display_name)
            
            # Store actual LaTeX in hidden data
            item.setData(Qt.UserRole, content)
            
            # Add checkbox
            item.setCheckState(Qt.Unchecked)
            
            # Add to list
            self.list_widget.addItem(item)
```

**`parser.py - extract_components()`**

```python
def extract_components(tex_content):
    all_items = []
    
    # Find all sections
    for match in re.finditer(r'\\section\{([^}]+)\}', tex_content):
        all_items.append({
            'pos': match.start(),  # Position: 150
            'type': 'section',
            'content': match.group(0),  # '\\section{Introduction}'
            'display': match.group(0)
        })
    
    # Find all math blocks
    for i, match in enumerate(re.finditer(r'\\\[.*?\\\]', tex_content, re.DOTALL), 1):
        all_items.append({
            'pos': match.start(),  # Position: 320
            'type': 'math',
            'content': match.group(0),  # '\\[ x = ... \\]'
            'display': f'[Equation {i}] ...'
        })
    
    # Sort by position
    all_items.sort(key=lambda x: x['pos'])
    
    # Convert to return format
    return [(item['type'], item['content'], item['display']) 
            for item in all_items]
```

### Example: Generating PDF

**User clicks "Generate PDF"**

**`gui.py - generate_tex_file()`**

```python
def generate_tex_file(self):
    selected = []
    
    # 1. Collect checked items
    for index in range(self.list_widget.count()):
        item = self.list_widget.item(index)
        if item.checkState() == Qt.Checked:
            # Get hidden LaTeX content
            content = item.data(Qt.UserRole)
            selected.append(content)
    
    if not selected:
        QMessageBox.warning(self, "Warning", "No components selected!")
        return
    
    # 2. Build LaTeX file
    build_tex(selected)
    
    # 3. Compile to PDF
    if compile_pdf():
        pdf_path = Path.cwd() / "output" / "output.pdf"
        QMessageBox.information(self, "Success", f"PDF at:\n{pdf_path}")
        
        # 4. Open PDF
        subprocess.run(["xdg-open", pdf_path])
```

**`builder.py - build_tex()`**

```python
def build_tex(selected):
    output_dir = Path.cwd() / "output"
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "output.tex", "w") as f:
        # Write preamble
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage[table]{xcolor}\n")
        f.write("\\usepackage{amsmath}\n")
        f.write("\\begin{document}\n\n")
        
        # Write selected components with formatting
        prev_type = None
        for comp in selected:
            current_type = get_component_type(comp)
            
            # Add smart spacing
            if current_type == 'section':
                f.write("\n")  # Extra line before sections
            
            f.write(f"{comp}\n")
            
            if current_type in ['section', 'subsection']:
                f.write("\n")  # Space after headings
            
            prev_type = current_type
        
        # Close document
        f.write("\n\\end{document}\n")
```

**`compiler.py - compile_pdf()`**

```python
def compile_pdf():
    output_dir = Path.cwd() / "output"
    tex_file = output_dir / "output.tex"
    
    # Verify file exists
    if not tex_file.exists():
        raise FileNotFoundError(f"File not found: {tex_file}")
    
    # Run pdflatex
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", 
         f"-output-directory={output_dir}", "output.tex"],
        cwd=str(output_dir),
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # Check if PDF was created
    pdf_path = output_dir / "output.pdf"
    if pdf_path.exists():
        print(f"✅ PDF generated: {pdf_path}")
        return True
    else:
        print(f"❌ Failed:\n{result.stdout}")
        return False
```

-----

## 🐛 Common Issues & Solutions

| Issue Description | Probable Cause | Solution |
| :--- | :--- | :--- |
| **"Module not found: src"** | Entry point in `setup.py` incorrect. | Use `latex-selector=main:main` not `latex-selector=src.main:main`. |
| **"Illegal pream-token (\\rowcolor)"** | `\rowcolor` extracted without table context. | Parser now extracts complete `\begin{tabular}...\end{tabular}` blocks. |
| **PDF path mismatch** | Compiler uses `src/output`, GUI expects `output/output.pdf`. | Both now use `Path.cwd() / "output"`. |
| **"Externally managed environment"** | System Python protected by PEP 668. | Use virtual environment (`source venv/bin/activate`). |

-----

## 🔧 Development Tips

### Adding New Component Types

1.  **Add regex pattern in `parser.py`:**

    ```python
    # Extract figures
    for i, match in enumerate(re.finditer(r'\\begin\{figure\}.*?\\end\{figure\}', 
                                           content, re.DOTALL), 1):
        figures.append({
            'pos': match.start(),
            'content': match.group(0),
            'name': f'[Figure {i}]'
        })
    ```

2.  **Add type detection in `builder.py`:**

    ```python
    def get_component_type(comp):
        # ... existing code ...
        elif '\\begin{figure}' in comp_lower:
            return 'figure'
    ```

3.  **Add spacing rules in `builder.py`:**

    ```python
    if current_type == 'figure':
        f.write("\n")  # Space before figures
    ```

### Debugging

  * **Enable verbose output in `compiler.py`:**

    ```python
    print(f"Running: pdflatex in {output_dir}")
    print(f"LaTeX output:\n{result.stdout}")
    ```

  * **Test parser independently:**

    ```python
    # test_parser.py
    from parser import extract_components

    with open('demo.tex', 'r') as f:
        components = extract_components(f.read())
        for comp in components:
            print(comp)
    ```

-----

## 📚 Further Reading

  * [PyQt5 Documentation](https://doc.qt.io/qtforpython/)
  * [LaTeX Documentation](https://www.latex-project.org/help/documentation/)
  * [Python Regex (re)](https://docs.python.org/3/library/re.html)
  * [setuptools Entry Points](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)

## 🎓 Learning Path

1.  **Beginner:** Understand user flow (load → select → generate).
2.  **Intermediate:** Modify parser to extract new component types.
3.  **Advanced:** Add preview panel showing LaTeX rendering.
4.  **Expert:** Implement drag-and-drop reordering of components.

-----

*Last Updated: November 2025*
*Python Version: 3.7+*
*PyQt5 Version: 5.15.7+*

```
```
