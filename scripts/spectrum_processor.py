
import subprocess
import sys
import tempfile

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Spectrum:
    intensities: np.ndarray
    wavenumbers: np.ndarray


def process_jdx(
    input_path: str | Path,
    ultrair_root: str | Path = "/app/UltraIR"
) -> Spectrum:

    input_path = Path(input_path).resolve()
    ultrair_root = Path(ultrair_root).resolve()

    # Проверяем входной файл
    if not input_path.is_file():
        raise FileNotFoundError(
            f"JDX file not found: {input_path}"
        )

    if input_path.suffix.lower() != ".jdx":
        raise ValueError("Expected a .jdx file")

    # Временные каталоги для официального конвертера
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)

        input_dir = temp_root / "input"
        output_dir = temp_root / "output"

        input_dir.mkdir()

        # Конвертер принимает директорию,
        # поэтому передаём ему только нужный файл
        import shutil
        shutil.copy2(
            input_path,
            input_dir / input_path.name
        )

        command = [
            sys.executable,
            "-m",
            "data.common.jcamp",
            "--input-dir", str(input_dir),
            "--output-dir", str(output_dir),
            "--target-points", "3600",
            "--low", "400",
            "--high", "4000",
        ]

        subprocess.run(
            command,
            cwd=ultrair_root,
            check=True
        )

        # Загружаем результат преобразования
        intensities = np.load(
            output_dir / "ir_norm.npy"
        )

        wavenumbers = np.load(
            output_dir / "wavenumbers.npy"
        )

    # Ожидаем ровно один спектр
    if intensities.shape != (1, 3600):
        raise ValueError(
            f"Unexpected spectrum shape: {intensities.shape}"
        )

    if wavenumbers.shape != (3600,):
        raise ValueError(
            f"Unexpected wavenumber shape: {wavenumbers.shape}"
        )

    if not np.isfinite(intensities).all():
        raise ValueError("Spectrum contains NaN or Inf")

    return Spectrum(
        intensities=intensities,
        wavenumbers=wavenumbers
    )
