import os

from groq import APIError

from rag.context_builder import build_context
from rag.prompt_builder import build_prompt
from rag.groq_client import generate_response


def generate_interpretation(prediction_path: str) -> str | None:
    if not os.getenv("GROQ_API_KEY"):
        return None

    context = build_context(prediction_path)
    prompt = build_prompt(context)

    try:
        return generate_response(prompt)
    except APIError:
        return None