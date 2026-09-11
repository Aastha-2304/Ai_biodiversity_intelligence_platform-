"""
Configuration Settings
Darukaa.Earth AI Biodiversity Intelligence Platform
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# API & Host Settings
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8000))
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

# CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "*"
]

# API Keys
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Data Paths
DATA_DIR = BASE_DIR / "data"
PROCESSED_CHUNKS_PATH = DATA_DIR / "processed_chunks.json"
INTERVENTIONS_PATH = DATA_DIR / "interventions.json"
DEMO_FALLBACK_PATH = DATA_DIR / "demo_fallback.json"
