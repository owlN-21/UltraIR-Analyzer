
import json
import numpy as np


def main():
    # Эталонные метки
    true_labels = np.load(
        "/app/UltraIR/data/functional_group_prediction/"
        "fold-demo/test/functional_groups.npy"
    )

    # Предсказания UltraIR
    with open(
        "/app/UltraIR/runs/predictions/functional_groups.json",
        encoding="utf-8"
    ) as file:
        results = json.load(file)

    class_names = results["class_names"]
    threshold = results["threshold"]

    # Восстанавливаем бинарные предсказания
    predictions = sorted(
        results["predictions"],
        key=lambda item: item["row_index"]
    )

    predicted_labels = np.array([
        [
            int(item["probabilities"][name] >= threshold)
            for name in class_names
        ]
        for item in predictions
    ])

    assert true_labels.shape == predicted_labels.shape

    # Для каждого спектра проверяем совпадение всех 17 меток
    exact_matches = np.all(
        true_labels == predicted_labels,
        axis=1
    )

    accuracy = np.mean(exact_matches)

    print(f"Количество спектров: {len(true_labels)}")
    print(f"Полных совпадений: {np.sum(exact_matches)}")
    print(f"Exact Match Accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    main()
