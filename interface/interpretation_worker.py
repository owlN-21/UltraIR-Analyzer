from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from rag.interpreter import generate_interpretation


class InterpretationWorker(QObject):

    finished = Signal(object)

    def __init__(self, prediction_path: str):
        super().__init__()

        self.prediction_path = Path(prediction_path)

    @Slot()
    def run(self):
        try:
            explanation = generate_interpretation(
                str(self.prediction_path)
            )

            self.finished.emit(explanation)

        except Exception:
            self.finished.emit(None)