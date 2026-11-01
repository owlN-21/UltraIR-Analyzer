
import argparse
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(
        description="Plot an infrared spectrum"
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--wavenumbers")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--name", default="spectrum")

    args = parser.parse_args()

    # Загружаем спектральные данные
    spectra = np.load(args.input)

    # Поддерживаем один спектр [L] и набор спектров [N, L]
    if spectra.ndim == 1:
        spectra = spectra[np.newaxis, :]

    if spectra.ndim != 2:
        raise ValueError(
            f"Expected [L] or [N, L], got {spectra.shape}"
        )

    if not 0 <= args.index < len(spectra):
        raise IndexError("Spectrum index is out of range")

    spectrum = spectra[args.index]

    # Загружаем физическую шкалу, если она предоставлена
    if args.wavenumbers:
        wavenumbers = np.load(args.wavenumbers)
    else:
        wavenumbers = np.linspace(
            400, 4000, len(spectrum)
        )

    if wavenumbers.ndim != 1:
        raise ValueError("Wavenumber axis must be 1D")

    if len(wavenumbers) != len(spectrum):
        raise ValueError(
            "Spectrum and wavenumber axis lengths differ"
        )

    # Создаём папку результатов
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{args.name}_spectrum.png"

    # Строим график
    plt.figure(figsize=(12, 5))

    plt.plot(
        wavenumbers,
        spectrum,
        color="royalblue",
        linewidth=1.5
    )

    plt.gca().invert_xaxis()

    plt.xlabel("Wavenumber (cm⁻¹)")
    plt.ylabel("Normalized signal")
    plt.title(f"IR Spectrum — {args.name}")

    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
