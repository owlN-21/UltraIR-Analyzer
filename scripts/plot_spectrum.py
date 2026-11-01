
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def main():
    spectra = np.load("/app/UltraIR/data/functional_group_prediction/fold-demo/test/ir_norm.npy")

    spectrum = spectra[0]

    wavenumbers = np.linspace(400, 4000, len(spectrum))

    plt.figure(figsize=(12, 5))
    plt.plot(wavenumbers, spectrum, color="royalblue")

    plt.gca().invert_xaxis()

    plt.xlabel("Wavenumber (cm⁻¹)")
    plt.ylabel("Normalized intensity")
    plt.title("UltraIR — NIST spectrum #0")

    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig("/app/research/results/spectrum_0.png", dpi=150)

    print("Saved: results/spectrum_0.png")


if __name__ == "__main__":
    main()
