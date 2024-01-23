from PySide6.QtCore import QThread, Signal

from nx.core.tcp_transfer import receive_file_tcp


class FileReceiverThread(QThread):
    update_progress = Signal(dict)
    finished_thread = Signal()
    finished_receiving = Signal()

    def __init__(self, port, file_dir, chunk_size, parent=None):
        super().__init__(parent)
        self.port = port
        self.file_dir = file_dir
        self.chunk_size = chunk_size

    def run(self):
        while not self.isInterruptionRequested():
            try:
                for progress in receive_file_tcp(
                    int(self.port), self.file_dir, self.chunk_size
                ):
                    if self.isInterruptionRequested():
                        break
                    self.update_progress.emit(progress)
                self.finished_receiving.emit()
                self.sleep(1)  # prevent the thread from running too fast
            except Exception as e:
                print(f"Error during file receiving: {e}")
                break
        self.finished_thread.emit()  # emit the signal when the thread is done
