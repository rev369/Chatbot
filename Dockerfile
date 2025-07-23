FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.2
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget ca-certificates gnupg build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl --http1.1 -fsSL https://ollama.com/install.sh | sh

# Pull phi3 model only (no server start here)
RUN ollama pull phi3:latest

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /Chatbot

COPY . .

RUN poetry install --no-root

EXPOSE 8090
EXPOSE 11434

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
