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
    QWidget,
)
from builder import build_tex
from parser import extract_components


class ComponentSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LaTeX Component Selector")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()
        self.label = QLabel("Select components")
        self.list_widget = QListWidget()
        self.load_button = QPushButton("Load .tex files")
        self.generate_button = QPushButton("Generate .tex file")

        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.load_button)
        layout.addWidget(self.generate_button)
        self.setLayout(layout)

        self.load_button.clicked.connect(self.load_tex_file)
        self.generate_button.clicked.connect(self.generate_tex_file)

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
                text = (
                    f"\\{comp[0]}{comp[1]}" if isinstance(comp, tuple) else f"\\{comp}"
                )
                item = QListWidgetItem(text)
                item.setCheckState(Qt.Unchecked)
                self.list_widget.addItem(item)

    def generate_tex_file(self):
        """Generate PDF from selected components."""
        selected = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())

        if not selected:
            QMessageBox.warning(self, "Warning", "No components selected!")
            return

        try:
            build_tex(selected)
            from compiler import compile_pdf
            if compile_pdf():
                pdf_path = Path("output/output.pdf").absolute()
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
