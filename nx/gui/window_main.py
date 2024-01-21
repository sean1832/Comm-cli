from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget

from nx.core import utilities as utils
from nx.gui import window_receive, window_send


class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Network File Exchange Tool")
        self.resize(400, 100)

        # Create a grid layout
        main_layout = QGridLayout(self)

        # Create a label in the window
        self.label = QLabel(f"IP: {utils.get_local_ip()}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font: Arial; font-size: 15px; black;")
        main_layout.addWidget(self.label, 0, 0, 1, 2)

        # Create a button in the window
        self.sender_btn = QPushButton("Sender")
        main_layout.addWidget(self.sender_btn, 1, 0)

        self.receiver_btn = QPushButton("Receiver")
        main_layout.addWidget(self.receiver_btn, 1, 1)

        # Connect button to function on_click
        self.sender_btn.clicked.connect(self.open_send_window)
        self.receiver_btn.clicked.connect(self.open_receiver_window)

        # Set the layout
        self.setLayout(main_layout)

    def open_send_window(self):
        self.app.send_window = window_send.SendWindow(app=self.app)
        self.app.send_window.show()

    def open_receiver_window(self):
        self.app.receive_window = window_receive.ReceiveWindow(app=self.app)
        self.app.receive_window.show()
