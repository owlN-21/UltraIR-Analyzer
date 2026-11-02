import sys
import logging
import runpy
import os

from pathlib import Path

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

    if len(sys.argv) >= 3 and sys.argv[1] == "--internal-module":

        module_name = sys.argv[2]

        allowed_modules = {
            "data.common.jcamp",
            "scripts.predict",
        }

        if module_name not in allowed_modules:
            raise ValueError(
                f"Unsupported internal module: {module_name}"
            )

        sys.argv = [module_name, *sys.argv[3:]]

        if getattr(sys, "frozen", False):

            # В GUI-сборке консольные потоки могут отсутствовать.
            # Предоставляем их библиотекам, использующим print/tqdm.
            if sys.stdout is None:
                sys.stdout = open(os.devnull, "w", encoding="utf-8")

            if sys.stderr is None:
                sys.stderr = open(os.devnull, "w", encoding="utf-8")

            ultrair_root = Path(sys._MEIPASS) / "UltraIR"

            module_files = {
                "data.common.jcamp": (
                    ultrair_root / "data" / "common" / "jcamp.py"
                ),
                "scripts.predict": (
                    ultrair_root / "scripts" / "predict.py"
                ),
            }

            sys.path.insert(0, str(ultrair_root))

            if module_name == "data.common.jcamp":
                runpy.run_module(
                    module_name,
                    run_name="__main__"
                )
            else:
                runpy.run_path(
                    str(module_files[module_name]),
                    run_name="__main__"
                )

        else:
            runpy.run_module(
                module_name,
                run_name="__main__"
            )

    else:
        main()