"""
Pydantic Schemas
Darukaa.Earth AI Biodiversity Intelligence Platform
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ImpactedMetric(BaseModel):
    metric_name: str
    baseline_value: Optional[str] = "Baseline"
    projected_value: Optional[str] = "Remediated"
    delta_estimate: Optional[str] = "Positive trajectory"
    time_horizon_years: Optional[str] = "1-3 years"
    causal_mechanism: Optional[str] = ""


class Recommendation(BaseModel):
    id: str
    name: str
    category: str
    action: str
    mechanism: str
    impacted_metrics: List[ImpactedMetric]
    time_horizon: str
    trade_offs: List[str] = []
    evidence_ids: List[str] = []
    applicable_biomes: Optional[List[str]] = []
    confidence: Optional[Dict[str, Any]] = None
    compatibility_status: Optional[str] = "Verified"
    compatibility_notes: Optional[List[str]] = []
    why_selected: Optional[str] = None


class EvidenceChunk(BaseModel):
    id: str
    title: str
    source: str
    year: int
    doi_or_ref: str
    excerpt: str
    chunk_text: Optional[str] = None
    metric_affected: Optional[str] = None
    practice: Optional[str] = None
    percent_improvement_range: Optional[str] = None
    timeframe: Optional[str] = None
    biome_applicability: List[str]
    is_dissenting: Optional[bool] = False
    evidence_strength: Optional[str] = "High"
    conflicting_with: Optional[str] = None
    relevance_score: Optional[float] = 1.0


class ClarifyingQuestion(BaseModel):
    missing_parameter: str
    question_text: str
    scientific_rationale: str
    suggested_inputs: Optional[List[str]] = []
    missing_parameters: Optional[List[str]] = []
    allow_custom_input: Optional[bool] = True
    custom_option_label: Optional[str] = " Type my own field values"
    custom_input_fields: Optional[List[Dict[str, Any]]] = []


class CausalHop(BaseModel):
    source_var: str
    relationship: str
    target_var: str
    evidence_citation: Optional[str] = None
    evidence_ref: Optional[str] = None
    scientific_principle: str


class ChatRequest(BaseModel):
    message: Optional[str] = None
    structured_input: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = "default_session"


class ChatResponse(BaseModel):
    session_id: str
    reply_markdown: str
    case_file_profile: Dict[str, Any]
    rule_metrics: Dict[str, Any]
    recommendations: List[Recommendation]
    retrieved_evidence: List[EvidenceChunk]
    causal_hops: List[CausalHop]
    clarifying_question: Optional[ClarifyingQuestion] = None
    stages: Optional[Dict[str, Any]] = None
    monitoring_plan: Optional[List[Dict[str, Any]]] = None
    suspicious_alerts: Optional[List[Dict[str, Any]]] = None
    contradiction_alerts: Optional[List[Dict[str, Any]]] = None
    running_assessment: Optional[str] = None
    completeness_score: Optional[float] = None
    input_mode_detected: Optional[str] = None
    is_cached: bool = False
    cached_timestamp: Optional[str] = None
    is_actionable: Optional[bool] = True
    requires_clarification: Optional[bool] = False
    spatial_context: Optional[Dict[str, Any]] = None
