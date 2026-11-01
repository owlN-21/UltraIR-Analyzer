
FROM python:3.11-slim

WORKDIR /app

RUN python --version

CMD ["python", "--version"]
