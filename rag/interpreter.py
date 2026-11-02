import logging
import os

from groq import APIError

from rag.context_builder import build_context
from rag.prompt_builder import build_prompt
from rag.groq_client import generate_response


logger = logging.getLogger(__name__)


def generate_interpretation(prediction_path: str) -> str | None:

    if not os.getenv("GROQ_API_KEY"):
        logger.warning("Groq API key is missing")
        return None

    logger.info("Starting RAG interpretation")

    try:
        context = build_context(prediction_path)
        prompt = build_prompt(context)

        explanation = generate_response(prompt)

        if explanation:
            logger.info("RAG interpretation completed")
        else:
            logger.warning("Groq returned empty response")

        return explanation or None

    except APIError as exc:
        logger.warning(
            "Groq API request failed: %s",
            type(exc).__name__
        )
        return None

    except FileNotFoundError:
        logger.exception("RAG file access failed")
        return None

    except Exception as exc:
        logger.error(
            "RAG interpretation failed: %s",
            type(exc).__name__
        )
        return None