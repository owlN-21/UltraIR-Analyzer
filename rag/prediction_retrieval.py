import json
from pathlib import Path

from rag.retriever import retrieve_groups


def retrieve_for_prediction(prediction_path: str | Path) -> list[dict]:
    prediction_path = Path(prediction_path)

    with prediction_path.open(encoding="utf-8-sig") as file:
        data = json.load(file)

    predictions = data["predictions"]

    if len(predictions) != 1:
        raise ValueError(
            "Ожидалось предсказание для одного спектра"
        )

    selected_labels = predictions[0]["selected_labels"]

    return retrieve_groups(selected_labels)