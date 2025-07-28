#!/bin/bash

# Create model directory if not exists
mkdir -p models

# Download the GGUF model if not already present
MODEL_PATH="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
MODEL_URL="https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

if [ ! -f "$MODEL_PATH" ]; then
  echo "Downloading model..."
  wget -O "$MODEL_PATH" "$MODEL_URL"
fi

# Start FastAPI app
uvicorn main:app --host 0.0.0.0 --port 10000
