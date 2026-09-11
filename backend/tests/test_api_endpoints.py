"""
FastAPI Endpoints Test: Health, Knowledge Base, and Multi-Turn Chat Clarification
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_api():
    print("--- 1. Testing /api/health & /api/knowledge-base ---")
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "online"
    print("[OK] /api/health returned online, indexed chunks:", data["knowledge_chunks_indexed"])

    r_kb = client.get("/api/knowledge-base")
    assert r_kb.status_code == 200
    kb = r_kb.json()
    assert kb["total_papers_indexed"] >= 10
    print(f"[OK] /api/knowledge-base returned {kb['total_papers_indexed']} papers, vocab dims: {kb['vocab_dimensions']}")

    print("\n--- 2. Testing Incomplete Chat via /api/chat ---")
    session_id = "test_api_session_1"
    chat_payload = {
        "session_id": session_id,
        "message": "Biodiversity is declining on my land"
    }
    r_chat = client.post("/api/chat", json=chat_payload)
    assert r_chat.status_code == 200
    res = r_chat.json()
    assert res["requires_clarification"] is True
    assert res["is_actionable"] is False
    assert res["clarifying_question"] is not None
    cq = res["clarifying_question"]
    assert "Soil Organic Carbon" in cq["question_text"]
    assert "rainfall pattern" in cq["question_text"].lower()
    assert "land use type" in cq["question_text"].lower()
    assert len(cq["suggested_inputs"]) >= 4
    assert cq["allow_custom_input"] is True
    print("[OK] Incomplete chat correctly returned clarifying question with options & custom input flag.")

    print("\n--- 3. Testing Turn 2 Clarification Submission via /api/chat ---")
    chat_payload_2 = {
        "session_id": session_id,
        "message": "Supplemental Field Telemetry: SOC 0.35%, rainfall 320mm unimodal, land use continuous wheat monoculture",
        "structured_input": {
            "soc_percent": 0.35,
            "rainfall_mm": 320.0,
            "current_crop": "wheat monoculture"
        }
    }
    r_chat_2 = client.post("/api/chat", json=chat_payload_2)
    assert r_chat_2.status_code == 200
    res_2 = r_chat_2.json()
    assert res_2["is_actionable"] is True
    assert res_2["requires_clarification"] is False
    assert len(res_2["recommendations"]) >= 2
    assert len(res_2["retrieved_evidence"]) >= 3
    print(f"[OK] Turn 2 successfully processed! Recommendations: {len(res_2['recommendations'])}, Evidence chunks: {len(res_2['retrieved_evidence'])}")

    print("\n[SUCCESS] ALL API ENDPOINT TESTS PASSED!")


if __name__ == "__main__":
    test_api()
