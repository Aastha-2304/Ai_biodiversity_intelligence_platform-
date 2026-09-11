"""
Response Cache & Demo Safety Manager
Darukaa.Earth AI Biodiversity Intelligence Platform
"""

import hashlib
import json
import os
import datetime
from typing import Dict, Any, Optional


class ResponseCache:
    """Hash-keyed response cache with offline demo fallback."""

    _CACHE_STORE: Dict[str, Dict[str, Any]] = {}
    _FALLBACK_STORE: Dict[str, Any] = {}

    @classmethod
    def initialize(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fallback_file = os.path.join(base_dir, "data", "demo_fallback.json")
        if os.path.exists(fallback_file):
            try:
                with open(fallback_file, "r", encoding="utf-8") as f:
                    cls._FALLBACK_STORE = json.load(f)
            except Exception:
                cls._FALLBACK_STORE = {}

    @classmethod
    def compute_signature(cls, query: str, profile: Dict[str, Any]) -> str:
        core = {
            "query": (query or "").strip().lower(),
            "soc": profile.get("soc_percent"),
            "rain": profile.get("rainfall_mm"),
            "biome": profile.get("biome"),
            "crop": profile.get("current_crop")
        }
        serialized = json.dumps(core, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def get(cls, signature: str) -> Optional[Dict[str, Any]]:
        return cls._CACHE_STORE.get(signature)

    @classmethod
    def set(cls, signature: str, response_data: Dict[str, Any]):
        cls._CACHE_STORE[signature] = {
            "cached_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "signature": signature,
            "data": response_data
        }

    @classmethod
    def get_canonical_demo(cls, demo_key: str = "canonical_semi_arid_wheat") -> Optional[Dict[str, Any]]:
        cls.initialize()
        return cls._FALLBACK_STORE.get(demo_key)
