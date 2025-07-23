# Use an official Python base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /Chatbot

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy local project files into the container
COPY . .

# Install dependencies (assumes pyproject.toml exists)
RUN poetry install --no-root

# Expose Streamlit port
EXPOSE 8090

# Run Streamlit app using poetry
CMD ["poetry", "run", "streamlit", "run", "chatbot.py", "--server.port=8090", "--server.address=0.0.0.0"]
