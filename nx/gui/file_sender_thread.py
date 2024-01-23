from PySide6.QtCore import QThread, Signal

from nx.core.tcp_transfer import send_file_tcp


class FileSenderThread(QThread):
    update_progress = Signal(dict)
    finished_sending = Signal()

    def __init__(self, ip, port, file_path, chunk_size, zip_mode, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.port = port
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.zip_mode = zip_mode

    def run(self):
        try:
            for progress in send_file_tcp(
                self.ip, int(self.port), self.file_path, self.chunk_size, self.zip_mode
            ):
                self.update_progress.emit(progress)
            self.finished_sending.emit()
        except Exception as e:
            print(f"Error during file sending: {e}")
