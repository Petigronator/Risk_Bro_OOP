#main.py

import sys
from PySide6.QtWidgets import QApplication
from GUI_Workflow import SM_GUI
import tracemalloc

def main():
    app = QApplication([])
    gui = SM_GUI()
    tracemalloc.start()
    gui.show()
    app.exec()

if __name__ == "__main__":
    main()