# Darukaa.Earth — AI Biodiversity Intelligence Platform

> **Hackathon Submission** — Evidence-Gated 9-Stage Ecological Decision Support System

## Architecture Overview

This system implements a **deterministic-first, LLM-explanation-only** pipeline. Every recommendation is calculated by rules before the LLM is ever called.

```
User Input
    │
    ▼
[Stage 0] Input Parser + Unit Bounds Validation
    │
    ▼
[Stage 1] Case File Session (Multi-turn Memory + Provenance)
    │
    ▼
[Stage 2] Completeness Check + Domain Probing
    │
    ▼
[Stage 3] Deterministic Rule Engine → Deficits, Risks, Hypotheses
    │
    ▼
[Stage 4] Biome-Gated Hybrid RAG (Evidence Retrieval + Dissenting Literature)
    │
    ▼
[Stage 5] Curated Intervention Library + Multi-Metric Causal Graph (3-hop)
    │
    ▼
[Stage 6] LLM Scientific Explanation (Numbers/Citations Pre-computed — LLM writes only)
    │
    ▼
[Stage 7] Peer-Review Verifier (Citation Check + Climate Compatibility + Confidence Score)
    │
    ▼
[Stage 8] Structured Output + On-Farm Monitoring Protocol
```

## Key Design Decisions

| Challenge | Our Solution |
|-----------|-------------|
| Generic LLM hallucinations | Rule engine computes all metrics BEFORE LLM is called |
| Single-variable shallow answers | 3-hop causal graph connects Soil ↔ Water ↔ Biodiversity |
| No evidence grounding | RAG retrieval from 10 curated peer-reviewed sources (FAO, IPCC, CSIRO, Nature) |
| Multi-turn memory loss | CaseFileSession with provenance tagging and contradiction detection |
| No confidence calibration | Mathematical confidence formula (not self-assertion) |

## Running Locally

### Backend (FastAPI)
```bash
# Install dependencies
pip install fastapi uvicorn pydantic anthropic

# Start the server
uvicorn backend.main:app --reload --port 8000
```

### Frontend (Vite/React)
```bash
cd frontend
npm install
npm run dev
# → Opens at http://localhost:5173
```

### Optional: Add Anthropic API Key
Create a `.env` file (or set in environment):
```
ANTHROPIC_API_KEY=your_api_key_here
```
Without a key, the system uses a fully deterministic template writer — still fully functional.

## Test Scenarios (Built-in)

| Scenario | Tests |
|----------|-------|
| 🌾 Canonical Semi-Arid Wheat | Full end-to-end — SOC 0.3%, 320mm rain, monoculture |
| ⚠️ Unit Sanity Test | Stage 0 bounds detection — 30% SOC flagged as suspicious |
| ⚡ Contradiction Test | Stage 1 multi-turn conflict — 1200mm in semi-arid biome |
| ❓ Incomplete Input | Stage 2 clarifying questions — missing critical variables |
| 🔍 Ambiguity Test | Stage 0 disambiguation — "soil is weak" → measurable metrics |

## Knowledge Base

10 peer-reviewed sources indexed:
- FAO Agroforestry Technical Guide 2021
- IPCC SRCCL Chapter 4 (2019)
- Nature Plants — Cereal-Legume Intercropping Meta-Analysis 2021
- ISRIC World Soil Information — Dryland Pedotransfer Functions 2020
- ICRISAT Semi-Arid Research Bulletin 2022
- FAO SOLAW 2021
- IPBES Land Degradation Assessment 2018
- FAO Soil Erosion Report 2019
- **CSIRO Dissenting Study** — Cover crop moisture trade-offs 2021
- IUCN Dryland Restoration Guidelines 2022

## Canonical Reference Case

**Input:** `SOC 0.3%, rainfall 320mm, monoculture wheat, semi-arid region`

**Expected Output:**
1. Aridity Index: 0.267 (Semi-arid)
2. SOC Deficit: -80% below 1.5% regional target
3. Biodiversity Index: 0.22 (Critical)
4. Recommendations: Agroforestry Shelterbelts + Legume Intercropping + Conservation Tillage
5. Evidence: FAO-AGROFORESTRY-2021, IPCC-SRCCL-2019-CH04, NATURE-ECOL-2021-INTERCROP
6. Confidence: High (≥0.85) with mathematical basis
