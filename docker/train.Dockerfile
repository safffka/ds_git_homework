FROM python:3.12-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install uv


COPY pyproject.toml uv.lock ./


RUN uv sync


COPY src ./src


ENV PYTHONPATH=/app/src



