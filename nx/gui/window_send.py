import os
import pathlib

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QWidget,
)

from nx.core import utilities as utils
from nx.gui.file_sender_thread import FileSenderThread
from nx.gui.widget_drop_area import DropArea
from nx.gui.window_add_entries import AddEntries


class SendWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.initUI()
        self.app = app
        self.file_path = None
        self.setWindowIcon(
            QIcon(str(pathlib.Path(utils.get_project_root(), "assets/icon.png")))
        )

    def initUI(self):
        # set the size of window
        self.resize(300, 300)

        # Create a grid layout
        main_layout = QGridLayout(self)

        # Create a ip combo box
        self.combo_box_ip = QComboBox()

        self.combo_box_ip.addItems(utils.read_local_entries("ips"))
        self.combo_box_ip.addItem("Add IP...")
        self.combo_box_ip.setEditable(True)
        self.combo_box_ip.currentIndexChanged.connect(self.on_combobox_ip_changed)
        main_layout.addWidget(self.combo_box_ip, 0, 0)

        # create a port combo box
        self.combo_box_port = QComboBox()
        self.combo_box_port.addItems(utils.read_local_entries("ports"))
        self.combo_box_port.addItem("Add Port...")
        self.combo_box_port.setEditable(True)
        self.combo_box_port.currentIndexChanged.connect(self.on_combobox_port_changed)
        main_layout.addWidget(self.combo_box_port, 0, 1)

        # Create a drop area
        self.drop_area = DropArea()
        main_layout.addWidget(self.drop_area, 2, 0, 1, 2)

        # create a clear button
        self.clear_btn = QPushButton("Clear")
        main_layout.addWidget(self.clear_btn, 3, 0, 1, 2)
        self.clear_btn.clicked.connect(self.clear)

        # create a send button
        self.send_btn = QPushButton("Send")
        main_layout.addWidget(self.send_btn, 4, 0, 1, 2)
        self.send_btn.clicked.connect(self.send_file)

        # create a progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar, 5, 0, 1, 2)

        # Set the layout
        self.setLayout(main_layout)
        self.setWindowTitle("Sender")

    def send_file(self):
        try:
            ip = self.combo_box_ip.currentText()
            port = self.combo_box_port.currentText()
            file_path = self.drop_area.file_path

            if ip == "":
                raise Exception("Please select an IP")
            if port == "":
                raise Exception("Please select a port")
            if file_path is None:
                raise Exception("Please select a file")

            is_dir = os.path.isdir(file_path)

            # Create and start the file sender thread
            self.file_sender_thread = FileSenderThread(
                ip, port, file_path, 4, is_dir, self
            )
            self.file_sender_thread.update_progress.connect(self.update_progress_bar)
            self.file_sender_thread.finished_sending.connect(self.on_sending_finished)
            self.file_sender_thread.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        if hasattr(self, "file_sender_thread") and self.file_sender_thread.isRunning():
            self.file_sender_thread.requestInterruption()
            self.file_sender_thread.terminate()
        super().closeEvent(event)

    @Slot(dict)
    def update_progress_bar(self, progress):
        current = progress["current"]
        total = progress["total"]
        percent = int((current / total) * 100)
        self.progress_bar.setValue(percent)

    @Slot()
    def on_sending_finished(self):
        print("done sending")
        self.progress_bar.setValue(100)

    def clear(self):
        self.drop_area.clear()
        self.progress_bar.setValue(0)

    def refresh_ip_combo_boxes(self):
        self.combo_box_ip.clear()
        self.combo_box_ip.addItems(utils.read_local_entries("ips"))
        self.combo_box_ip.addItem("Add IP...")
        # select the second last item
        self.combo_box_ip.setCurrentIndex(self.combo_box_ip.count() - 2)

    def refresh_port_combo_boxes(self):
        self.combo_box_port.clear()
        self.combo_box_port.addItems(utils.read_local_entries("ports"))
        self.combo_box_port.addItem("Add Port...")
        # select the second last item
        self.combo_box_port.setCurrentIndex(self.combo_box_port.count() - 2)

    def on_combobox_ip_changed(self):
        if self.combo_box_ip.currentText() == "Add IP...":
            self.add_ip()

    def on_combobox_port_changed(self):
        if self.combo_box_port.currentText() == "Add Port...":
            self.add_port()

    def add_ip(self):
        self.combo_box_ip.setCurrentIndex(0)
        self.app.add_entries = AddEntries("IP", "ips", self)
        self.app.add_entries.entries_updated.connect(self.refresh_ip_combo_boxes)
        self.app.add_entries.show()

    def add_port(self):
        self.combo_box_port.setCurrentIndex(0)
        self.app.add_entries = AddEntries("Port", "ports", self)
        self.app.add_entries.entries_updated.connect(self.refresh_port_combo_boxes)
        self.app.add_entries.show()
