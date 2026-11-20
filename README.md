# 💡 AI Grant & Funding Finder for Startups
### Powered by IBM Granite AI &nbsp;|&nbsp; Problem Statement
https://aigrantfundingfinder-7jhbubnvtwmnm4dwohj2ot.streamlit.app/

> **Technology mandate met:** IBM Cloud Lite + IBM Granite (`ibm/granite-13b-instruct-v2`) via `ibm-watsonx-ai` SDK

---

## Overview

A full-stack AI-powered **Streamlit** application that helps startups discover personalised grant and funding opportunities and auto-generates tailored application proposals using IBM Granite AI.

### Key Features

| Feature | Description |
|---|---|
| **Personalised Matching** | Startup profile → ranked grants (domain, stage, location, keyword scoring) |
| **IBM Granite Proposals** | AI-generated full proposals or individual sections (executive summary, problem, solution, impact, budget) |
| **Eligibility Q&A** | Ask natural-language questions; IBM Granite answers based on grant criteria |
| **22+ Curated Grants** | Real-world grants: India (SISFS, BIRAC, TIDE, AIM, NIDHI), USA (SBIR, NSF, DOE), EU (EIC, Horizon), UK, Global |
| **Browse & Filter** | Browse all grants, filter by domain / stage / location |
| **Streamlit UI** | Dark-themed, animated IBM Carbon-inspired UI built with Streamlit |
| **Fallback Mode** | Template-based responses when IBM credentials are absent — all features remain functional |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│              Streamlit Frontend  (app.py)                │
│  Sidebar (Startup Profile)                               │
│  Tab 1: 🎯 Personalised Matches                          │
│  Tab 2: 📋 Browse All Grants                             │
│  Tab 3: ❓ Eligibility Q&A                               │
└────────────────────┬─────────────────────────────────────┘
                     │ Python function calls
┌────────────────────▼─────────────────────────────────────┐
│                  backend/                                │
│  matcher.py        — personalised ranking engine         │
│  granite_service.py — IBM Granite AI integration         │
│  grant_database.py  — 22+ curated grants                 │
│  models.py          — Pydantic data models               │
│  config.py          — environment / credential config    │
└──────────────┬──────────────────┬────────────────────────┘
               │                  │
┌──────────────▼──────┐  ┌────────▼───────────────────────┐
│  Grant Database     │  │   IBM Granite (watsonx.ai)      │
│  22+ real-world     │  │   ibm/granite-13b-instruct-v2   │
│  grants (seed data) │  │   IBM Cloud Lite Credentials    │
└─────────────────────┘  └────────────────────────────────┘
```

---

## Grants Covered

| Region | Grants |
|---|---|
| 🇮🇳 India | SISFS, BIRAC BioNEST, TIDE 2.0, NIDHI PRAYAS, AIM/AIC, AgriUdaan, RBI Regulatory Sandbox, NASSCOM DeepTech |
| 🇺🇸 USA | SBIR/STTR, NSF I-Corps, DOE Clean Energy Fund |
| 🇪🇺 Europe | EIC Accelerator, Horizon Europe (MSCA), ClimateLaunchpad |
| 🇬🇧 UK | Wellcome Innovator Awards |
| 🌍 Global | IBM Hyper Protect Accelerator, Google Black Founders Fund, Microsoft Founders Hub, AWS Activate, World Bank infoDev, UNEP Climate Innovation, Gates Foundation EdTech |

---

## Setup & Run

### 1. Clone / Navigate to Project

```bash
cd "AICTE_Funding_finderfor_staartup"
```

### 2. Configure IBM Credentials

```bash
cp .env.example .env
# Edit .env and fill in:
#   IBM_API_KEY=<your IBM Cloud API key>
#   IBM_PROJECT_ID=<your watsonx.ai project ID>
```

> **Get free credentials:** Sign up at [ibm.com/cloud](https://cloud.ibm.com) → Create API Key → Create watsonx.ai project (Free Lite tier available)

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
# App available at http://localhost:8501
```

Alternatively, use the helper runner:

```bash
python run.py
```

---

## IBM Granite Integration

The system uses the `ibm-watsonx-ai` SDK to call **IBM Granite 13B Instruct** for three tasks:

### Proposal Generation
```python
from backend.granite_service import generate_proposal_section

result = generate_proposal_section(
    grant=grant,
    startup=startup,
    section="full"   # or: executive_summary | problem_statement | solution | impact | budget
)
```

### Eligibility Q&A
```python
from backend.granite_service import answer_eligibility_question

answer = answer_eligibility_question(
    grant=grant,
    startup=startup,
    question="Are we eligible if founded 2 years ago?"
)
```

### Startup Summary
```python
from backend.granite_service import generate_startup_summary

summary = generate_startup_summary(startup=startup_profile)
```

> **Without IBM credentials:** The system falls back to deterministic template-based responses — all features remain functional.

---

## Run Tests

```bash
python test_matcher.py
# OR
python -m pytest test_matcher.py -v
```

Tests cover: grant loading, ranking sort order, domain / stage / location matching, score bounds, `min_score` filtering, and match reasons.

---

## Project Structure

```
AICTE_Funding_finderfor_staartup/
├── app.py                     # Streamlit app — UI, tabs, sidebar, rendering
├── run.py                     # Helper runner script
├── requirements.txt           # Python dependencies
├── .env.example               # IBM credentials template
├── test_matcher.py            # Unit tests (pytest-compatible)
└── backend/
    ├── __init__.py
    ├── config.py              # Environment config (IBM_API_KEY, IBM_PROJECT_ID)
    ├── models.py              # Pydantic models: StartupProfile, GrantOpportunity, ProposalOutput
    ├── grant_database.py      # 22+ curated grants (seed data, easily extensible)
    ├── matcher.py             # Personalised ranking engine (domain/stage/location/keyword scoring)
    └── granite_service.py     # IBM Granite AI integration (proposals, Q&A, summaries)
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `ibm-watsonx-ai` | IBM Granite model inference |
| `pydantic` | Data validation & models |
| `python-dotenv` | `.env` credential loading |
| `sentence-transformers` | Semantic similarity scoring |
| `scikit-learn` | ML utilities for matching |
| `fastapi` + `uvicorn` | Optional REST API layer |
| `feedparser` | RSS feed parsing for live grant discovery |
| `beautifulsoup4` + `lxml` | Web scraping utilities |

---

## Usage Example

### Startup Profile Input (Sidebar)

| Field | Example |
|---|---|
| Startup Name | FarmSense AI |
| Industry Domain | AgriTech |
| Stage | Seed |
| Location | India |
| Description | IoT-based soil monitoring for smallholder farmers |
| Team Size | 8 |
| Keywords | precision farming, IoT, rural |

### What Happens Next

1. **AI Matching** — the engine scores all 22+ grants using domain, stage, location & keyword signals
2. **Ranked Results** — grants sorted by relevance score with clear match reasons
3. **IBM Granite Summary** — your startup is summarised by Granite AI
4. **Generate Proposal** — click ✨ Generate inside any grant card to produce a tailored draft

---

## IBM Cloud Lite — What's Used

| IBM Service | Usage |
|---|---|
| **IBM Cloud API Key** | Authentication for all IBM services |
| **IBM watsonx.ai** | Granite model inference endpoint |
| **IBM Granite 13B Instruct** | Proposal generation, eligibility Q&A, startup summaries |

All services available on **IBM Cloud Lite (free tier)**.

---

## Screenshots

| Tab | Description |
|---|---|
| 🎯 Personalised Matches | Ranked grant cards with match scores, reasons, and AI proposal generator |
| 📋 Browse All Grants | Full grant library with domain / stage / location filters |
| ❓ Eligibility Q&A | Select a grant, ask a question, get an IBM Granite answer |

---

*Problem Statement #18 — AI Grant & Funding Finder for Startups*  
*AICTE Hackathon | IBM Cloud Lite + IBM Granite Mandatory*
