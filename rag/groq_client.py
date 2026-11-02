import os
from groq import Groq


MODEL = "qwen/qwen3.8-27b"


def generate_response(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Не задан GROQ_API_KEY")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_completion_tokens=800,
    )

    return response.choices[0].message.content or ""