#!/usr/bin/env python3
"""
Download script for TinyLlama model
"""

import os
import requests
from pathlib import Path

MODEL_URL = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
MODEL_PATH = Path("models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

def download_model():
    """Download the TinyLlama model"""
    os.makedirs("models", exist_ok=True)

    if MODEL_PATH.exists():
        print(f"Model already exists at {MODEL_PATH}")
        return

    print("Downloading TinyLlama 1.1B model... This may take a few minutes.")

    try:
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(MODEL_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(".1f")

        print(f"Model downloaded successfully to {MODEL_PATH}")

    except Exception as e:
        print(f"Error downloading model: {e}")
        print("Please download manually from: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF")

if __name__ == "__main__":
    download_model()