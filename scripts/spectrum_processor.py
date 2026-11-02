
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
    ultrair_root: str | Path = (
        Path(sys._MEIPASS) / "UltraIR"
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parents[2] / "UltraIR"
    )
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
            "--internal-module" if getattr(sys, "frozen", False) else "-m",
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

        # Проверяем, что измеряется по оси Y
        jdx_text = input_path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        is_transmittance = any(
            line.strip().upper() == "##YUNITS=TRANSMITTANCE"
            for line in jdx_text.splitlines()
        )

        # # Эксперимент: меняем направление полос
        # if is_transmittance:
        #     intensities = 1.0 - intensities
        #     print("Transmittance spectrum: signal inverted")

        if is_transmittance:
            sys.path.insert(0, str(ultrair_root))
            from data.common.jcamp import parse_jcamp

            axis, transmittance = parse_jcamp(input_path)

            if np.any(transmittance <= 0) or np.any(transmittance > 1):
                raise ValueError("Expected transmittance in (0, 1]")

            absorbance = -np.log10(transmittance)

            mask = (
                (axis >= 400) &
                (axis <= 4000)
            )

            if np.count_nonzero(mask) < 2:
                raise ValueError("Not enough spectrum points")

            values = np.interp(
                wavenumbers,
                axis[mask],
                absorbance[mask]
            )

            minimum = values.min()
            maximum = values.max()

            if maximum <= minimum:
                raise ValueError("Cannot normalize spectrum")

            intensities = (
                (values - minimum) / (maximum - minimum)
            ).astype(np.float32)[np.newaxis, :]

            print("Transmittance converted to absorbance")


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
