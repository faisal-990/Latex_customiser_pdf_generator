import os
import sys
import subprocess
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from builder import build_tex
from parser import extract_components
from compiler import compile_pdf


class ComponentSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LaTeX Component Selector")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()
        self.label = QLabel("Select components")
        self.list_widget = QListWidget()
        self.load_button = QPushButton("Load .tex files")
        
        # Create horizontal layout for generate buttons
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate PDF")
        self.view_tex_button = QPushButton("View Output .tex")
        self.view_tex_button.setEnabled(False)  # Disabled until tex is generated
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.view_tex_button)

        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.load_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.load_button.clicked.connect(self.load_tex_file)
        self.generate_button.clicked.connect(self.generate_tex_file)
        self.view_tex_button.clicked.connect(self.view_output_tex)

    def load_tex_file(self):
        """Load a LaTeX file and extract components."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open .tex files", "", "TeX files (*.tex)"
        )
        if not file_path:
            return

        with open(file_path, "r") as f:
            content = f.read()
            components = extract_components(content)
            self.list_widget.clear()
            for comp in components:
                # comp is now a tuple: (type, content, display_name)
                if len(comp) == 3:
                    _, content, display_name = comp
                    item = QListWidgetItem(display_name)
                    item.setData(Qt.UserRole, content)  # Store actual content
                else:
                    # Fallback for old format
                    text = f"\\{comp[0]}{comp[1]}" if isinstance(comp, tuple) else f"\\{comp}"
                    item = QListWidgetItem(text)
                    item.setData(Qt.UserRole, text)
                
                item.setCheckState(Qt.Unchecked)
                self.list_widget.addItem(item)

    def generate_tex_file(self):
        """Generate PDF from selected components."""
        selected = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.checkState() == Qt.Checked:
                # Get the actual content stored in UserRole
                content = item.data(Qt.UserRole)
                selected.append(content)

        if not selected:
            QMessageBox.warning(self, "Warning", "No components selected!")
            return

        try:
            build_tex(selected)
            self.view_tex_button.setEnabled(True)  # Enable view button
            
            if compile_pdf():
                pdf_path = (Path.cwd() / "output" / "output.pdf").absolute()
                QMessageBox.information(
                    self, "Success", f"PDF generated at:\n{pdf_path}"
                )
                if sys.platform == "win32":
                    os.startfile(pdf_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", pdf_path])
                else:
                    subprocess.run(["xdg-open", pdf_path])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF:\n{str(e)}")

    def view_output_tex(self):
        """Open the generated .tex file in default text editor."""
        tex_path = (Path.cwd() / "output" / "output.tex").absolute()
        
        if not tex_path.exists():
            QMessageBox.warning(self, "Warning", "output.tex not found! Generate it first.")
            return
        
        try:
            if sys.platform == "win32":
                os.startfile(tex_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", tex_path])
            else:
                # Linux - try common text editors
                subprocess.run(["xdg-open", tex_path])
        except Exception as e:
            QMessageBox.information(
                self, 
                "File Location", 
                f"Could not open automatically.\n\nFile location:\n{tex_path}"
            )

