import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from src.gui import ComponentSelector
import signal

def main():
    # Create output directory if it doesn't exist
   ## (Path(__file__).parent / "output").mkdir(exist_ok=True)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = ComponentSelector()
    window.show()
    app.setQuitOnLastWindowClosed(True)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
