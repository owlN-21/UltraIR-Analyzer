
import json
import subprocess
import sys
import tempfile

from pathlib import Path

import numpy as np

from scripts.spectrum_processor import Spectrum


class UltraIRPredictor:

    def __init__(
        self,
        ultrair_root: str | Path = (
            Path(sys._MEIPASS) / "UltraIR"
            if getattr(sys, "frozen", False)
            else Path(__file__).resolve().parents[2] / "UltraIR"
        )
    ):
        self.ultrair_root = Path(ultrair_root).resolve()

        self.config = (
            "configs/functional_group_prediction/nist.yaml"
        )

        self.checkpoint = (
            "checkpoints/functional_group_prediction/"
            "ultrair_nist.pt"
        )

    def predict(self, spectrum: Spectrum) -> dict:

        intensities = spectrum.intensities

        # Проверяем форму входного массива
        if intensities.ndim != 2:
            raise ValueError(
                "Expected spectrum shape [N, L]"
            )

        if intensities.shape[0] != 1:
            raise ValueError(
                "Expected exactly one spectrum"
            )

        if not np.isfinite(intensities).all():
            raise ValueError(
                "Spectrum contains NaN or Inf"
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)

            input_path = temp_root / "spectrum.npy"
            output_path = temp_root / "prediction.json"

            # Сохраняем массив для официального CLI
            np.save(input_path, intensities)

            command = [
                sys.executable,
                "--internal-module" if getattr(sys, "frozen", False) else "-m",
                "scripts.predict",
                "--config", self.config,
                "--ckpt", self.checkpoint,
                "--input", str(input_path),
                "--output", str(output_path),
                "--device", "cpu",
                "--batch-size", "1",
            ]

            subprocess.run(
                command,
                cwd=self.ultrair_root,
                check=True
            )

            # Читаем оригинальный JSON UltraIR
            with open(
                output_path,
                encoding="utf-8"
            ) as file:
                prediction = json.load(file)

        return prediction
