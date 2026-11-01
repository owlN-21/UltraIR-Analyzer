from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from scripts.pipeline import analyze_jdx


class AnalysisWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    progress = Signal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    @Slot()
    def run(self):
        try:
            self.progress.emit("Анализ спектра...")

            result_dir = analyze_jdx(
                Path(self.file_path)
            )

            self.finished.emit(str(result_dir))

        except Exception as exc:
            self.error.emit(str(exc))