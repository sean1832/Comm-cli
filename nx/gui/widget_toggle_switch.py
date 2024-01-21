import pathlib

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QCheckBox

from nx.core.utilities import get_project_root


class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img_width = 128  # Define the width
        self.img_height = 128  # Define the height

        # Convert the paths to string with forward slashes
        self.img_on = pathlib.Path(
            get_project_root(), "gui/assets/toggle_on.png"
        ).as_posix()  # must be in posix format
        self.img_off = pathlib.Path(
            get_project_root(), "gui/assets/toggle_off.png"
        ).as_posix()  # must be in posix format

        print(f"Image On Path: {self.img_on}")

        self.setStyleSheet(
            f"""
            QCheckBox {{
                spacing: 5px;
            }}

            QCheckBox::indicator {{
                width: {self.img_width}px;
                height: {self.img_height}px;
            }}

            QCheckBox::indicator:unchecked {{
                image: url({self.img_off});
            }}

            QCheckBox::indicator:unchecked:hover {{
                image: url({self.img_off});
            }}

            QCheckBox::indicator:unchecked:pressed {{
                image: url({self.img_off});
            }}

            QCheckBox::indicator:checked {{
                image: url({self.img_on});
            }}

            QCheckBox::indicator:checked:hover {{
                image: url({self.img_on});
            }}

            QCheckBox::indicator:checked:pressed {{
                image: url({self.img_on});
            }}

            QCheckBox::indicator:indeterminate:hover {{
                image: url({self.img_on});
            }}

            QCheckBox::indicator:indeterminate:pressed {{
                image: url({self.img_on});
            }}
        """
        )

    def sizeHint(self):
        return QSize(128, 128)
