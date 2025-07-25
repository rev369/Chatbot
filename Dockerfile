# Start from a minimal Linux base with Python 3.12
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.2
ENV PATH="/root/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates \
    gnupg \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Install Ollama
# -------------------------------
RUN curl RUN curl --http1.1 -fsSL https://ollama.com/install.sh | sh


# Pull phi3 model
RUN ollama serve & \
    sleep 5 && \
    ollama pull phi3:latest


# -------------------------------
# Install Poetry
# -------------------------------
RUN curl -sSL https://install.python-poetry.org | python3 -

# -------------------------------
# Set working directory
# -------------------------------
WORKDIR /Chatbot

# Copy all project files into the container
COPY . .

# Install Python dependencies using Poetry
RUN poetry install --no-root

# Expose Streamlit port
EXPOSE 8090

# Run Streamlit via Poetry
  CMD ["streamlit", "run", "chatbot.py", "--server.address", "0.0.0.0", "--server.port", "8090"]
