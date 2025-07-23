#!/bin/bash

# Start Ollama server in the background
ollama serve &

# Wait for Ollama server to be ready (adjust sleep as needed)
sleep 10

# Run Streamlit binding to 0.0.0.0 so it’s accessible externally
exec poetry run streamlit run chatbot.py --server.address 0.0.0.0 --server.port 8090
