
import argparse
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def plot_spectrum(
    intensities: np.ndarray,
    wavenumbers: np.ndarray,
    output_path: str | Path,
    title: str = "IR Spectrum"
) -> None:
    """Build and save an infrared spectrum plot."""

    intensities = np.asarray(intensities)
    wavenumbers = np.asarray(wavenumbers)

    if intensities.ndim != 1:
        raise ValueError("Intensities must be a 1D array")

    if wavenumbers.ndim != 1:
        raise ValueError("Wavenumbers must be a 1D array")

    if len(intensities) != len(wavenumbers):
        raise ValueError(
            "Spectrum and wavenumber axis lengths differ"
        )

    if not (
        np.isfinite(intensities).all()
        and np.isfinite(wavenumbers).all()
    ):
        raise ValueError("Spectrum contains NaN or Inf")

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        wavenumbers,
        intensities,
        color="royalblue",
        linewidth=1.5
    )

    ax.invert_xaxis()

    ax.set_xlabel("Wavenumber (cm⁻¹)")
    ax.set_ylabel("Normalized signal")
    ax.set_title(title)

    ax.grid(alpha=0.3)
    fig.tight_layout()

    try:
        fig.savefig(output_path, dpi=150)
    finally:
        plt.close(fig)


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

    spectra = np.load(args.input)

    if spectra.ndim == 1:
        spectra = spectra[np.newaxis, :]

    if spectra.ndim != 2:
        raise ValueError(
            f"Expected [L] or [N, L], got {spectra.shape}"
        )

    if not 0 <= args.index < len(spectra):
        raise IndexError("Spectrum index is out of range")

    spectrum = spectra[args.index]

    if args.wavenumbers:
        wavenumbers = np.load(args.wavenumbers)
    else:
        wavenumbers = np.linspace(
            400, 4000, len(spectrum)
        )

    output_path = (
        Path(args.output_dir)
        / f"{args.name}_spectrum.png"
    )

    plot_spectrum(
        intensities=spectrum,
        wavenumbers=wavenumbers,
        output_path=output_path,
        title=f"IR Spectrum — {args.name}"
    )

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
