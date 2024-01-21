import sys

from PySide6.QtWidgets import QApplication

from nx.gui.window_main import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
