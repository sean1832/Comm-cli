import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QLabel


class DropArea(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Drop files here")
        self.file_path = None
        self.setStyleSheet(
            """
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 10px;
            }
            """
        )
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self.setText(os.path.basename(path))
            self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            self.file_path = path
            print(path)

    def clear(self):
        self.setText("Drop files here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_path = None
