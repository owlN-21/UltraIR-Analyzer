import json
from pathlib import Path


KNOWLEDGE_BASE_PATH = (
    Path(__file__).resolve().parent
    / "knowledge_base"
    / "ir_reference.json"
)


def load_knowledge_base() -> dict:
    with open(KNOWLEDGE_BASE_PATH, encoding="utf-8") as file:
        data = json.load(file)

    return {
        group["class_name"]: group
        for group in data["functional_groups"]
    }

def retrieve_groups(class_names: list[str]) -> list[dict]:
    knowledge_base = load_knowledge_base()

    results = []

    for class_name in class_names:
        group = knowledge_base.get(class_name)

        if group is not None:
            results.append(group)

    return results