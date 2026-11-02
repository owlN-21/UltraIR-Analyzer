import sys
import logging

from PySide6.QtWidgets import QApplication

from interface.main_window import MainWindow


def main():

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%H:%M:%S"
    )

    logging.info("Starting UltraIR Analyzer")

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()