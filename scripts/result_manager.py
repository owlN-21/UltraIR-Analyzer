
import json
import re
import tempfile

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from scripts.spectrum_processor import Spectrum


class ResultManager:

    def __init__(self, output_root: str | Path = "results"):
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)

    def _next_candidate_number(self) -> int:
        numbers = []

        for path in self.output_root.iterdir():
            if not path.is_dir():
                continue

            match = re.fullmatch(
                r"candidate(\d+)",
                path.name
            )

            if match:
                number = int(match.group(1))

                if number > 0:
                    numbers.append(number)

        return max(numbers, default=0) + 1

    def _save_plot(
        self,
        spectrum: Spectrum,
        output_path: Path
    ) -> None:

        intensities = spectrum.intensities[0]
        wavenumbers = spectrum.wavenumbers

        plt.figure(figsize=(12, 5))

        plt.plot(
            wavenumbers,
            intensities,
            color="royalblue"
        )

        plt.gca().invert_xaxis()

        plt.xlabel("Wavenumber (cm⁻¹)")
        plt.ylabel("Normalized signal")
        plt.title("IR Spectrum")

        plt.grid(alpha=0.3)
        plt.tight_layout()

        plt.savefig(output_path, dpi=150)
        plt.close()

    def save(
        self,
        spectrum: Spectrum,
        prediction: dict
    ) -> Path:

        # Временная папка внутри results
        with tempfile.TemporaryDirectory(
            prefix=".pending-",
            dir=self.output_root
        ) as temp_dir:

            temp_path = Path(temp_dir)

            # Сохраняем оригинальный JSON UltraIR
            prediction_path = temp_path / "prediction.json"

            with open(
                prediction_path,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    prediction,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            # Сохраняем график
            self._save_plot(
                spectrum,
                temp_path / "spectrum.png"
            )

            # Выбираем следующий номер
            number = self._next_candidate_number()

            final_path = (
                self.output_root / f"candidate{number}"
            )

            if final_path.exists():
                raise FileExistsError(
                    f"Candidate already exists: {final_path}"
                )

            # Публикуем завершённый результат
            temp_path.rename(final_path)

            return final_path
