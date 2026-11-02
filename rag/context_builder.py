import json
from pathlib import Path

from rag.prediction_retrieval import retrieve_for_prediction


def build_context(prediction_path: str | Path) -> dict:
    prediction_path = Path(prediction_path)

    with prediction_path.open(encoding="utf-8-sig") as file:
        data = json.load(file)

    prediction = data["predictions"][0]

    groups = retrieve_for_prediction(prediction_path)

    return {
        "model": "UltraIR",
        "prediction_type": data["prediction_type"],
        "threshold": data["threshold"],
        "selected_labels": prediction["selected_labels"],
        "model_scores": prediction["probabilities"],
        "reference_data": groups,
        "observed_peaks": None
    }