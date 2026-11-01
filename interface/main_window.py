from pathlib import Path

from PySide6.QtGui import QPixmap

import json

from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QHBoxLayout,
)

from interface.analysis_worker import AnalysisWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UltraIR Analyzer")
        self.resize(1300, 800)

        self.selected_file = None
        self.result_dir = None
        self.thread = None
        self.worker = None

        # Главный контейнер
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ЛЕВАЯ ПАНЕЛЬ
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)

        title = QLabel("UltraIR Analyzer")
        title.setStyleSheet(
            "font-size: 26px; font-weight: bold;"
        )

        self.select_button = QPushButton("Выбрать JDX-файл")
        self.select_button.setFixedHeight(45)
        self.select_button.clicked.connect(self.select_file)

        self.file_label = QLabel("Файл не выбран")
        self.file_label.setWordWrap(True)

        self.analyze_button = QPushButton("Анализировать")
        self.analyze_button.setFixedHeight(45)
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.start_analysis)

        self.status_label = QLabel("Ожидание файла")
        self.status_label.setWordWrap(True)

        # Будущий блок предсказаний
        predictions_title = QLabel("Результаты UltraIR")
        predictions_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        self.predictions_label = QLabel(
            "Здесь появятся предсказанные "
            "функциональные группы"
        )
        self.predictions_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.predictions_label.setWordWrap(True)
        self.predictions_label.setStyleSheet(
            "background-color: #ffffff;"
            "border: 1px solid #dddddd;"
            "border-radius: 8px;"
            "padding: 20px;"
        )

        left_layout.addWidget(title)
        left_layout.addWidget(self.select_button)
        left_layout.addWidget(self.file_label)
        left_layout.addWidget(self.analyze_button)
        left_layout.addWidget(self.status_label)
        left_layout.addSpacing(20)
        left_layout.addWidget(predictions_title)
        left_layout.addWidget(self.predictions_label, stretch=1)

        # ПРАВАЯ ПАНЕЛЬ
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        spectrum_title = QLabel("ИК-спектр")
        spectrum_title.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        self.spectrum_label = QLabel(
            "Здесь появится график спектра"
        )
        self.spectrum_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.spectrum_scroll = QScrollArea()
        self.spectrum_scroll.setWidgetResizable(True)
        self.spectrum_scroll.setWidget(self.spectrum_label)

        right_layout.addWidget(spectrum_title)
        right_layout.addWidget(self.spectrum_scroll, stretch=1)

        # Соотношение ширины панелей
        main_layout.addWidget(left_panel, stretch=35)
        main_layout.addWidget(right_panel, stretch=65)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите ИК-спектр",
            "",
            "JCAMP-DX files (*.jdx)"
        )

        if file_path:
            self.selected_file = Path(file_path)
            self.result_dir = None

            self.file_label.setText(
                f"Выбран файл: {self.selected_file.name}"
            )

            self.status_label.setText("Готов к анализу")
            self.analyze_button.setEnabled(True)

    def start_analysis(self):
        if self.selected_file is None:
            return

        self.analyze_button.setEnabled(False)
        self.select_button.setEnabled(False)
        self.status_label.setText("Запуск анализа...")

        self.thread = QThread()
        self.worker = AnalysisWorker(str(self.selected_file))

        # Переносим обработчик в отдельный поток
        self.worker.moveToThread(self.thread)

        # Подключаем сигналы
        self.thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.status_label.setText)
        self.worker.finished.connect(self.analysis_finished)
        self.worker.error.connect(self.analysis_error)

        # Завершение потока
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.analysis_cleanup)

        self.thread.start()

    def analysis_finished(self, result_dir: str):
        self.result_dir = Path(result_dir)

        self.status_label.setText(
            f"Анализ завершён: {self.result_dir.name}"
        )

        self.display_spectrum()
        self.display_predictions()

    def analysis_error(self, error_message: str):
        self.status_label.setText("Ошибка анализа")

        QMessageBox.critical(
            self,
            "Ошибка UltraIR",
            error_message
        )

    def analysis_cleanup(self):
        self.thread = None
        self.worker = None

        self.select_button.setEnabled(True)
        self.analyze_button.setEnabled(
            self.selected_file is not None
        )

    def closeEvent(self, event):
        if self.thread is not None and self.thread.isRunning():
            QMessageBox.information(
                self,
                "Анализ выполняется",
                "Дождитесь завершения анализа перед закрытием."
            )
            event.ignore()
            return

        event.accept()


    def display_spectrum(self):
        if self.result_dir is None:
            return

        image_path = self.result_dir / "spectrum.png"

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            self.spectrum_label.setText(
                "Не удалось загрузить график"
            )
            return

        scaled_pixmap = pixmap.scaled(
            950,
            400,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.spectrum_label.setPixmap(scaled_pixmap)

    def display_predictions(self):
        if self.result_dir is None:
            return

        json_path = self.result_dir / "prediction.json"

        if not json_path.is_file():
            self.predictions_label.setText(
                "Файл prediction.json не найден"
            )
            return

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        prediction = data["predictions"][0]

        selected_labels = prediction["selected_labels"]
        scores = prediction["probabilities"]

        if not selected_labels:
            self.predictions_label.setText(
                "Функциональные группы не обнаружены"
            )
            return

        lines = []

        for group in selected_labels:
            score = scores[group]

            lines.append(
                f"{group}: {score:.4f}"
            )

        self.predictions_label.setText(
            "\n".join(lines)
        )