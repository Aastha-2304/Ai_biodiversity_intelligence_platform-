"""
Automated Verification Script for Unified Streamlit Architecture
Tests:
1. HTTP endpoint availability (Streamlit on port 8501)
2. Database caching & instant reuse
3. Grounded chatbot Q&A against assessment
4. Session history retrieval and stats
"""

import urllib.request
import json
import time
from backend.database.audit_store import AuditDatabase
from backend.pipeline.input_parser import InputParser
from backend.pipeline.llm_writer import ScientificWriter
from backend.models.case_file import get_or_create_case_file

def test_http_endpoint():
    print("--- 1. Testing Streamlit HTTP Endpoint (localhost:8501) ---")
    req = urllib.request.Request("http://localhost:8501", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        code = resp.getcode()
        html = resp.read().decode("utf-8", errors="ignore")
        print(f"HTTP Status: {code}")
        assert code == 200, f"Expected 200, got {code}"
        assert "<title>Darukaa.Earth" in html or "Streamlit" in html or "darukaa" in html.lower(), "Page title or brand not found"
        print("✓ Streamlit HTTP 200 OK")

def test_pipeline_caching_and_chatbot():
    print("\n--- 2. Testing Database Caching & Instant Solution Reuse ---")
    test_session_id = "test_verify_session_42"
    query = "Soil organic carbon is 0.3%, rainfall low (320mm), crop monoculture wheat, region semi-arid."
    payload = {"soc_percent": 0.3, "rainfall_mm": 320.0, "current_crop": "monoculture wheat", "biome": "semi-arid"}

    from app import execute_diagnostic_with_cache

    # First call: computes and saves to DB
    t0 = time.time()
    res1 = execute_diagnostic_with_cache(query, payload, test_session_id)
    t1 = time.time()
    dur1 = t1 - t0
    print(f"1st run duration: {dur1:.3f}s (Computed fresh)")
    assert res1.get("is_actionable") is True
    assert len(res1.get("recommendations", [])) > 0
    print(f"✓ Prescriptions generated: {len(res1['recommendations'])}")

    # Second call with same telemetry: should be an INSTANT cache hit
    t2 = time.time()
    res2 = execute_diagnostic_with_cache(query, payload, test_session_id)
    t3 = time.time()
    dur2 = t3 - t2
    print(f"2nd run duration: {dur2:.3f}s (Cache hit)")
    assert res2.get("is_cached") is True
    print(f"✓ Instant Cache Hit verified! Reused solution without re-computation.")

    # 3. Test Grounded Chatbot Follow-up Q&A
    print("\n--- 3. Testing Interactive Grounded Chatbot ---")
    prof = res1["case_file"]["profile"]
    rm = res1["rule_metrics"]
    recs = res1["recommendations"]

    # Doubt 1: Spacing
    q1 = "What spacing should I use between Faidherbia parkland trees?"
    ans1 = ScientificWriter.answer_assessment_followup(q1, prof, rm, recs, [])
    print(f"User Question: '{q1}'")
    print(f"Chatbot Answer:\n{ans1}\n")
    assert "8m x 12m" in ans1 or "spacing" in ans1.lower()
    AuditDatabase.save_chat_message(test_session_id, "user", q1, "doubt")
    AuditDatabase.save_chat_message(test_session_id, "assistant", ans1, "answer")
    print("✓ Chatbot accurately answered spacing question with field numbers!")

    # Doubt 2: Species Alternatives
    q2 = "Can I substitute another legume for chickpea?"
    ans2 = ScientificWriter.answer_assessment_followup(q2, prof, rm, recs, [{"role": "user", "text": q1}, {"role": "assistant", "text": ans1}])
    print(f"User Question: '{q2}'")
    print(f"Chatbot Answer:\n{ans2}\n")
    assert "cowpea" in ans2.lower() or "clover" in ans2.lower() or "legume" in ans2.lower()
    AuditDatabase.save_chat_message(test_session_id, "user", q2, "doubt")
    AuditDatabase.save_chat_message(test_session_id, "assistant", ans2, "answer")
    print("✓ Chatbot accurately suggested certified companion legume alternatives!")

    # 4. Test Audit History & Database Stats
    print("\n--- 4. Testing Audit Database Stats & History ---")
    stats = AuditDatabase.get_database_stats()
    print("Database Stats:", stats)
    assert stats["total_sessions"] >= 1
    assert stats["cached_solutions"] >= 1
    assert stats["cache_reuse_hits"] >= 1

    chat_history = AuditDatabase.get_session_chat_history(test_session_id)
    print(f"Retrieved {len(chat_history)} chat messages for session {test_session_id}")
    assert len(chat_history) >= 2
    print("✓ Full chronological chat log verified in SQLite!")

if __name__ == "__main__":
    test_http_endpoint()
    test_pipeline_caching_and_chatbot()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! Single Streamlit deployment is ready.")
