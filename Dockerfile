FROM python:3.11-slim

WORKDIR /app/UltraIR

COPY --from=ultrair-source . .

RUN python -m pip install --no-cache-dir -e .

RUN python -m pip install --no-cache-dir matplotlib

CMD ["python", "-m", "scripts.predict", "--help"]