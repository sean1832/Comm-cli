import os
import pathlib

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)

from nx.core import utilities as utils


class AddEntries(QDialog):
    entries_updated = Signal()

    def __init__(self, name, data_source: str, parent=None):
        super().__init__(parent)
        self.data_source = data_source
        self.name = name
        self.initUI()
        self.setWindowIcon(
            QIcon(str(pathlib.Path(utils.get_project_root(), "assets/icon.png")))
        )

    def initUI(self):
        self.setWindowTitle(f"Add {self.name}")
        self.resize(300, 200)

        # set focus to the window
        self.setModal(True)

        # Create a grid layout
        main_layout = QGridLayout(self)

        # Create table widget
        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels([f"{self.name}s"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # populate table
        items = utils.read_local_entries(self.data_source)
        if len(items) == 0:
            items = [""]
        for row, item in enumerate(items):
            self.table.insertRow(row)
            checkbox = QTableWidgetItem(item)
            checkbox.setFlags(checkbox.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, checkbox)

        # create add row button
        self.add_row_btn = QPushButton("Add Row")
        self.add_row_btn.clicked.connect(self.add_row)

        # create delete button
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_items)

        # create save button
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_items)

        # layout
        main_layout.addWidget(self.table, 0, 0, 1, 2)
        main_layout.addWidget(self.add_row_btn, 1, 0)
        main_layout.addWidget(self.delete_btn, 1, 1)
        main_layout.addWidget(self.save_btn, 2, 0, 1, 2)

        # Set the layout
        self.setLayout(main_layout)

    def delete_items(self):
        # reversed so that the row numbers don't change
        for row in reversed(range(self.table.rowCount())):
            # if not none
            if self.table.item(row, 0) is not None:
                if self.table.item(row, 0).checkState() == Qt.CheckState.Checked:
                    item = self.table.item(row, 0).text()
                    print(f"Deleting {item}")
                    self.table.removeRow(row)

    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        checkbox = QTableWidgetItem(f"Item {row+1}")
        checkbox.setFlags(checkbox.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.table.setItem(row, 0, checkbox)

    def read_table(self):
        items = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0).text()
            items.append(item)
        return items

    def save_items(self):
        items = self.read_table()
        root = utils.get_appdata_root()
        data_file = os.path.join(root, self.data_source)
        utils.write_json(data_file, items)
        self.entries_updated.emit()
        self.close()
