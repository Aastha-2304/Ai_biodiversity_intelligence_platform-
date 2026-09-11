"""
Persistent Audit Store & Intelligence Database Module
Darukaa.Earth AI Biodiversity Intelligence Platform

Manages persistent SQLite storage for:
1. Multi-turn consultation sessions and chat histories
2. Cached assessments with normalized telemetry signatures for instant reuse
3. Longitudinal environmental case files and recommendations
"""

import sqlite3
import json
import hashlib
import os
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "darukaa_audit.db"


class AuditDatabase:
    """Manages SQLite persistent storage for sessions, assessments, and query caching."""

    _initialized = False

    @classmethod
    def _get_connection(cls) -> sqlite3.Connection:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def initialize(cls):
        """Initializes database tables if they do not exist."""
        if cls._initialized:
            return

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            
            # Sessions Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                title TEXT,
                ecosystem_type TEXT,
                health_score REAL,
                summary TEXT,
                query_count INTEGER DEFAULT 1,
                result_json TEXT
            )
            """)

            # Migrate existing databases: add result_json column if missing
            try:
                cursor.execute("ALTER TABLE sessions ADD COLUMN result_json TEXT")
                conn.commit()
            except sqlite3.OperationalError:
                pass  # Column already exists

            # Assessments Cache Table (Normalized telemetry hash for instant reuse)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signature TEXT UNIQUE NOT NULL,
                ecosystem_type TEXT NOT NULL,
                query_text TEXT,
                input_payload_json TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_accessed_at TEXT NOT NULL,
                hit_count INTEGER DEFAULT 1
            )
            """)

            # Chat Messages Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message_text TEXT NOT NULL,
                context_type TEXT DEFAULT 'general',
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
            """)

            # Indices for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessments_sig ON assessments (signature)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_messages (session_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_updated ON sessions (updated_at DESC)")

            conn.commit()

        cls._initialized = True

    @classmethod
    def compute_telemetry_signature(cls, query: str, profile: Dict[str, Any]) -> str:
        """
        Computes a normalized ecological signature from query keywords and field telemetry.
        Enables instant reuse when the same conditions are presented.
        """
        eco = (profile.get("ecosystem_type") or "agricultural").lower()
        
        # Normalize key numeric parameters (rounded to prevent minor float mismatches)
        soc = round(float(profile.get("soc_percent", 0.0)), 2) if profile.get("soc_percent") is not None else None
        rain = round(float(profile.get("rainfall_mm", 0.0)) / 10.0) * 10 if profile.get("rainfall_mm") is not None else None
        crop = (profile.get("current_crop") or profile.get("land_use_type") or "").strip().lower()
        biome = (profile.get("biome") or "").strip().lower()
        pollution = (profile.get("pollution_level") or "").strip().lower()
        water_qual = (profile.get("water_quality") or "").strip().lower()
        canopy = round(float(profile.get("canopy_cover_pct", 0.0))) if profile.get("canopy_cover_pct") is not None else None

        normalized_payload = {
            "eco": eco,
            "soc": soc,
            "rain": rain,
            "crop": crop,
            "biome": biome,
            "pollution": pollution,
            "water_qual": water_qual,
            "canopy": canopy
        }

        # If payload is empty of telemetry, hash the query text
        clean_query = " ".join((query or "").strip().lower().split())
        
        sig_data = {
            "payload": normalized_payload,
            "query_core": clean_query[:80]
        }
        serialized = json.dumps(sig_data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:20]

    @classmethod
    def get_cached_assessment(cls, query: str, profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Checks if an identical or matching ecological assessment was already solved."""
        cls.initialize()
        sig = cls.compute_telemetry_signature(query, profile)

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT result_json, hit_count, created_at 
            FROM assessments 
            WHERE signature = ?
            """, (sig,))
            row = cursor.fetchone()
            if row:
                # Update hit count & last accessed
                now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
                cursor.execute("""
                UPDATE assessments 
                SET hit_count = hit_count + 1, last_accessed_at = ? 
                WHERE signature = ?
                """, (now_str, sig))
                conn.commit()

                try:
                    result = json.loads(row["result_json"])
                    result["is_cached"] = True
                    result["cached_hit_count"] = row["hit_count"] + 1
                    result["cached_since"] = row["created_at"]
                    return result
                except Exception:
                    return None

        return None

    @classmethod
    def save_assessment(
        cls,
        session_id: str,
        query: str,
        profile: Dict[str, Any],
        result: Dict[str, Any]
    ) -> str:
        """Persists the solved ecological assessment and updates session metadata."""
        cls.initialize()
        sig = cls.compute_telemetry_signature(query, profile)
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        eco = (profile.get("ecosystem_type") or result.get("rule_metrics", {}).get("ecosystem_type") or "agricultural").lower()
        health = float(result.get("rule_metrics", {}).get("system_health_index") or 40.0)

        # Generate summary title
        crop = profile.get("current_crop") or f"{eco.title()} Site"
        title = f"{eco.title()}: {crop.title()}"
        if profile.get("soc_percent") is not None:
            title += f" (SOC {profile['soc_percent']}%)"

        summary = result.get("rule_metrics", {}).get("diagnostic_hypothesis") or (
            f"Evaluated {eco} ecosystem with {len(result.get('recommendations', []))} actionable prescriptions."
        )

        with cls._get_connection() as conn:
            cursor = conn.cursor()

            # Upsert into assessments table
            payload_json = json.dumps(profile)
            result_json = json.dumps(result)
            cursor.execute("""
            INSERT INTO assessments (signature, ecosystem_type, query_text, input_payload_json, result_json, created_at, last_accessed_at, hit_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(signature) DO UPDATE SET
                hit_count = hit_count + 1,
                last_accessed_at = excluded.last_accessed_at,
                result_json = excluded.result_json
            """, (sig, eco, query, payload_json, result_json, now_str, now_str))

            # Upsert into sessions table — also store latest result_json for fast session restore
            cursor.execute("""
            INSERT INTO sessions (session_id, created_at, updated_at, title, ecosystem_type, health_score, summary, query_count, result_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                updated_at = excluded.updated_at,
                title = excluded.title,
                ecosystem_type = excluded.ecosystem_type,
                health_score = excluded.health_score,
                summary = excluded.summary,
                query_count = query_count + 1,
                result_json = excluded.result_json
            """, (session_id, now_str, now_str, title, eco, health, summary, result_json))

            conn.commit()

        return sig

    @classmethod
    def save_chat_message(
        cls,
        session_id: str,
        role: str,
        message_text: str,
        context_type: str = "general"
    ):
        """Saves a message to the persistent chat history."""
        cls.initialize()
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO chat_messages (session_id, role, message_text, context_type, created_at)
            VALUES (?, ?, ?, ?, ?)
            """, (session_id, role, message_text, context_type, now_str))
            
            cursor.execute("""
            UPDATE sessions SET updated_at = ? WHERE session_id = ?
            """, (now_str, session_id))
            conn.commit()

    @classmethod
    def get_session_chat_history(cls, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves chronological chat messages for a session."""
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT role, message_text, context_type, created_at
            FROM chat_messages
            WHERE session_id = ?
            ORDER BY id ASC
            """, (session_id,))
            rows = cursor.fetchall()
            return [
                {
                    "role": r["role"],
                    "text": r["message_text"],
                    "context_type": r["context_type"],
                    "time": r["created_at"]
                }
                for r in rows
            ]

    @classmethod
    def list_recent_sessions(cls, limit: int = 25) -> List[Dict[str, Any]]:
        """Lists recently active consultation sessions."""
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT session_id, created_at, updated_at, title, ecosystem_type, health_score, summary, query_count
            FROM sessions
            ORDER BY updated_at DESC
            LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    @classmethod
    def get_session_last_result(cls, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the exact assessment result stored for a specific session.
        Used to restore full dashboard state when switching between sessions.
        """
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            # Primary: use the result_json stored directly on the session row
            cursor.execute("""
            SELECT result_json, updated_at
            FROM sessions
            WHERE session_id = ?
            """, (session_id,))
            row = cursor.fetchone()
            if row and row["result_json"]:
                try:
                    result = json.loads(row["result_json"])
                    result["is_cached"] = True
                    result["cached_since"] = row["updated_at"]
                    return result
                except Exception:
                    pass

            # Fallback: join on ecosystem_type to find a nearby assessment
            cursor.execute("""
            SELECT a.result_json, a.hit_count, a.created_at
            FROM assessments a
            INNER JOIN sessions s ON s.ecosystem_type = a.ecosystem_type
            WHERE s.session_id = ?
            ORDER BY a.last_accessed_at DESC
            LIMIT 1
            """, (session_id,))
            row2 = cursor.fetchone()
            if row2:
                try:
                    result = json.loads(row2["result_json"])
                    result["is_cached"] = True
                    result["cached_hit_count"] = row2["hit_count"]
                    result["cached_since"] = row2["created_at"]
                    return result
                except Exception:
                    return None
        return None

    @classmethod
    def get_database_stats(cls) -> Dict[str, Any]:
        """Provides statistics on cached solutions and total consultations."""
        cls.initialize()
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sessions")
            total_sessions = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*), SUM(hit_count) FROM assessments")
            c_row = cursor.fetchone()
            total_assessments = c_row[0] or 0
            total_hits = c_row[1] or 0

            cursor.execute("SELECT COUNT(*) FROM chat_messages")
            total_messages = cursor.fetchone()[0]

            return {
                "total_sessions": total_sessions,
                "cached_solutions": total_assessments,
                "cache_reuse_hits": total_hits,
                "total_messages": total_messages
            }
