import base64
import os
import time
from pathlib import Path
from typing import Dict, Optional
import requests
import json
import gradio as gr
import uuid
from elevenlabs import generate, play, set_api_key


def encode_image(img_path):
    if not img_path:
        return None
    with open(img_path, "rb") as fin:
        image_data = base64.b64encode(fin.read()).decode("utf-8")
    return image_data


def get_latest_files(directory: str, file_types: list = ['.webm', '.zip']) -> Dict[str, Optional[str]]:
    """Get the latest recording and trace files"""
    latest_files: Dict[str, Optional[str]] = {ext: None for ext in file_types}

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        return latest_files

    for file_type in file_types:
        try:
            matches = list(Path(directory).rglob(f"*{file_type}"))
            if matches:
                latest = max(matches, key=lambda p: p.stat().st_mtime)
                # Only return files that are complete (not being written)
                if time.time() - latest.stat().st_mtime > 1.0:
                    latest_files[file_type] = str(latest)
        except Exception as e:
            print(f"Error getting latest {file_type} file: {e}")

    return latest_files


def text_to_speech_eleven_labs(text: str, api_key: str = None, voice_id: str = None, language: str = "en"):
    if api_key:
        set_api_key(api_key)
    else:
        # If API key is not provided, it will try to use the environment variable ELEVEN_API_KEY
        pass

    if not api_key and not os.getenv("ELEVEN_API_KEY") and not os.getenv("ELEVEN_LABS_API_KEY"):
        print("Eleven Labs API key not found. Please set ELEVEN_API_KEY or ELEVEN_LABS_API_KEY in .env or provide it.")
        return

    try:
        # Eleven Labs API supports 'model' parameter for language selection
        # For Hindi, you might need a specific model or voice that supports it.
        # Assuming 'eleven_multilingual_v2' or similar supports multiple languages.
        # The 'voice' parameter is for the specific voice, 'model' for language/quality.
        model_name = "eleven_multilingual_v2" if language == "hi" else "eleven_v2"
        audio = generate(text=text, voice=voice_id if voice_id else "Rachael", model=model_name)
        play(audio)
    except Exception as e:
        print(f"Error generating or playing audio: {e}")
