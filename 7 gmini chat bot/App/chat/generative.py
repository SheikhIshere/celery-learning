"""
Generative wrapper for Google Gemini (gmini).

This module tries to use the official `google.generativeai` SDK if available. If not,
it falls back to a minimal REST `requests` example. Configure GEMINI_API_KEY in env.

The wrapper exposes:

generate_reply(prompt: str, conversation_history: list[dict]) -> dict

Return value:
{ 'text': str, 'raw': dict }

Note: Update MODEL_NAME to the exact model string you intend to use (example placeholders provided).
"""

from __future__ import annotations
import os
import json
from typing import List, Dict, Any
from google import generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Replace with the exact model you want. Examples (update to current names):
# MODEL_NAME = 'models/text-bison-001'  # example for text-based models
# MODEL_NAME = 'gemini-1.0'  # placeholder
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/text-bison-001")


def _use_official_sdk(prompt: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError("Official google.generativeai SDK not installed.")

    genai.api_key = GEMINI_API_KEY

    # Combine conversation history into a single prompt string
    combined = "\n".join(
        [f"{m.get('role')}: {m.get('content')}" for m in conversation_history] + [f"user: {prompt}"]
    )

    # Generate response (adjust based on actual SDK method signature)
    resp = genai.generate_text(model=MODEL_NAME, prompt=combined, max_output_tokens=512)

    # Parse response
    text = ""
    raw: Dict[str, Any] = {}
    try:
        if hasattr(resp, "text"):
            text = resp.text
            raw = resp
        elif isinstance(resp, dict):
            raw = resp
            text = resp.get("output") or resp.get("candidates", [{}])[0].get("output", "")
        else:
            return _use_rest_fallback(prompt, conversation_history)
    except Exception:
        return _use_rest_fallback(prompt, conversation_history)

    return {"text": text, "raw": raw}


def _use_rest_fallback(prompt: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Minimal fallback using requests if SDK is unavailable.
    """
    import requests

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set in environment.")

    url = f"https://api.generativeai.googleapis.com/v1/{MODEL_NAME}:generateText"

    payload = {
        "prompt": "\n".join([f"{m.get('role')}: {m.get('content')}" for m in conversation_history] + [f"user: {prompt}"]),
        "maxOutputTokens": 512,
    }

    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()

    # Extract text from common response structure
    text = data.get("output") or data.get("candidates", [{}])[0].get("output", "")
    return {"text": text, "raw": data}


def generate_reply(prompt: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Public method to generate a reply using Gemini SDK or REST fallback.
    """
    try:
        return _use_official_sdk(prompt, conversation_history)
    except Exception:
        return _use_rest_fallback(prompt, conversation_history)
