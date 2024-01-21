from PySide6.QtCore import QThread, Signal

from nx.core.tcp_transfer import receive_file_tcp


class FileReceiverThread(QThread):
    update_progress = Signal(dict)
    finished_receiving = Signal()

    def __init__(self, port, file_dir, chunk_size):
        super().__init__()
        self.port = port
        self.file_dir = file_dir
        self.chunk_size = chunk_size

    def run(self):
        try:
            for progress in receive_file_tcp(
                int(self.port), self.file_dir, self.chunk_size
            ):
                self.update_progress.emit(progress)
            self.finished_receiving.emit()
        except Exception as e:
            print(f"Error during file receiving: {e}")
