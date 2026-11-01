
import argparse
from pathlib import Path

from scripts.spectrum_processor import process_jdx
from scripts.ultrair_predictor import UltraIRPredictor
from scripts.result_manager import ResultManager


def analyze_jdx(input_path: str | Path) -> Path:

    # 1. Подготовка спектра
    print("[1/3] Processing JDX spectrum...")

    spectrum = process_jdx(input_path)

    # 2. Предсказание UltraIR
    print("[2/3] Running UltraIR prediction...")

    predictor = UltraIRPredictor()
    prediction = predictor.predict(spectrum)

    # 3. Сохранение результатов
    print("[3/3] Saving results...")

    manager = ResultManager("results")

    result_dir = manager.save(
        spectrum=spectrum,
        prediction=prediction
    )

    print(f"Analysis completed: {result_dir}")

    return result_dir


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a JDX spectrum using UltraIR"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input JDX file"
    )

    args = parser.parse_args()

    analyze_jdx(args.input)


if __name__ == "__main__":
    main()
