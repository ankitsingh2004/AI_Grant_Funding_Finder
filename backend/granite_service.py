"""
granite_service.py — IBM Granite AI integration via ibm-watsonx-ai SDK.

Responsibilities:
  1. Authenticate with IBM Cloud using API key (IAM token exchange).
  2. Call ibm/granite-13b-instruct-v2 (or configured model) for:
     - Startup summary generation
     - Proposal / application draft generation (full or by section)
     - Grant eligibility Q&A
"""
from __future__ import annotations
import logging
from typing import Optional
from backend.config import IBM_API_KEY, IBM_PROJECT_ID, IBM_WATSONX_URL, GRANITE_MODEL_ID
from backend.models import GrantOpportunity, StartupProfile, ProposalResponse

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy-initialise the watsonx Model (avoids import-time failures if creds
# are not yet configured).
# ---------------------------------------------------------------------------
_model = None


def _get_model():
    global _model
    if _model is not None:
        return _model

    if not IBM_API_KEY or IBM_API_KEY == "your_ibm_api_key_here":
        logger.warning(
            "IBM_API_KEY not configured — Granite AI features will return "
            "placeholder responses. Set IBM_API_KEY in .env to enable."
        )
        return None

    try:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as Params

        credentials = Credentials(
            url=IBM_WATSONX_URL,
            api_key=IBM_API_KEY,
        )

        _model = ModelInference(
            model_id=GRANITE_MODEL_ID,
            credentials=credentials,
            project_id=IBM_PROJECT_ID,
            params={
                Params.DECODING_METHOD: "greedy",
                Params.MAX_NEW_TOKENS: 1024,
                Params.MIN_NEW_TOKENS: 50,
                Params.REPETITION_PENALTY: 1.1,
            },
        )
        logger.info("IBM Granite model initialised: %s", GRANITE_MODEL_ID)
        return _model

    except Exception as exc:
        logger.error("Failed to initialise IBM Granite model: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

_SUMMARY_PROMPT = """\
You are a startup funding advisor. Given the startup profile below, write a \
concise 2-sentence professional summary that highlights the startup's unique value \
proposition and why it is fundable.

Startup Name: {name}
Domain: {domain}
Stage: {stage}
Location: {location}
Description: {description}

Professional Summary:"""


_PROPOSAL_SECTION_PROMPTS = {
    "executive_summary": """\
Write a compelling executive summary (150–200 words) for a grant application.
Grant: {grant_title} (source: {grant_source})
Startup: {startup_name} — {startup_domain} at {startup_stage} stage in {startup_location}.
Description: {startup_description}
Executive Summary:""",

    "problem_statement": """\
Write a clear problem statement (150–200 words) for a grant application.
Grant: {grant_title}
Startup: {startup_name} — {startup_description}
Problem Statement:""",

    "solution": """\
Write a detailed solution section (200–250 words) for a grant application.
Grant: {grant_title}
Startup: {startup_name} — {startup_description}
Solution:""",

    "impact": """\
Write an impact and outcomes section (150–200 words) for a grant application.
Grant: {grant_title}, Funding: {funding_amount}
Startup: {startup_name} in {startup_domain} at {startup_stage}
Impact & Outcomes:""",

    "budget": """\
Write a high-level budget justification (100–150 words) for a grant application.
Grant: {grant_title}, Available Funding: {funding_amount}
Startup Stage: {startup_stage}, Team Size: {team_size}
Budget Justification:""",
}


_FULL_PROPOSAL_PROMPT = """\
You are an expert grant writer helping a startup apply for funding.
Write a structured grant application proposal with the following sections:
1. Executive Summary
2. Problem Statement
3. Proposed Solution
4. Expected Impact & Outcomes
5. Budget Overview

Grant: {grant_title} — {grant_source}
Funding Available: {funding_amount}
Eligibility: {eligibility}
Startup Name: {startup_name}
Domain: {startup_domain}
Stage: {startup_stage}
Location: {startup_location}
Description: {startup_description}

Important: Keep each section clearly labeled. Be specific, professional, and concise.
Total length: 500–700 words.

Grant Application Proposal:"""


def _call_granite(prompt: str) -> Optional[str]:
    """
    Call IBM Granite and return the generated text, or None on error.
    Falls back to a placeholder when the model is not configured.
    """
    model = _get_model()
    if model is None:
        return None  # caller handles fallback

    try:
        response = model.generate_text(prompt=prompt)
        # ibm-watsonx-ai returns a string directly from generate_text
        return response.strip() if isinstance(response, str) else str(response).strip()
    except Exception as exc:
        logger.error("Granite generation error: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_startup_summary(startup: StartupProfile) -> str:
    """
    Generate a professional one-paragraph summary of the startup using Granite.
    Falls back to a template-based summary if Granite is unavailable.
    """
    prompt = _SUMMARY_PROMPT.format(
        name=startup.name,
        domain=startup.domain,
        stage=startup.stage,
        location=startup.location,
        description=startup.description,
    )
    result = _call_granite(prompt)
    if result:
        return result

    # Fallback — deterministic template
    return (
        f"{startup.name} is a {startup.stage}-stage {startup.domain} startup "
        f"based in {startup.location}. "
        f"{startup.description[:200]}{'...' if len(startup.description) > 200 else ''}"
    )


def generate_proposal_section(
    grant: GrantOpportunity,
    startup: StartupProfile,
    section: str = "full",
) -> ProposalResponse:
    """
    Generate a grant application section (or full proposal) using IBM Granite.
    Returns a ProposalResponse with content and metadata.
    """
    common_vars = {
        "grant_title": grant.title,
        "grant_source": grant.source,
        "funding_amount": grant.funding_amount,
        "eligibility": grant.eligibility,
        "startup_name": startup.name,
        "startup_domain": startup.domain,
        "startup_stage": startup.stage,
        "startup_location": startup.location,
        "startup_description": startup.description,
        "team_size": str(startup.team_size or "Not specified"),
    }

    if section == "full":
        prompt = _FULL_PROPOSAL_PROMPT.format(**common_vars)
    elif section in _PROPOSAL_SECTION_PROMPTS:
        prompt = _PROPOSAL_SECTION_PROMPTS[section].format(**common_vars)
    else:
        prompt = _FULL_PROPOSAL_PROMPT.format(**common_vars)
        section = "full"

    result = _call_granite(prompt)

    if result:
        content = result
    else:
        # Fallback template when Granite is not configured
        content = _fallback_proposal(grant, startup, section)

    return ProposalResponse(
        section=section,
        content=content,
        word_count=len(content.split()),
    )


def _fallback_proposal(
    grant: GrantOpportunity,
    startup: StartupProfile,
    section: str,
) -> str:
    """Template-based fallback when IBM Granite is not available."""
    if section == "executive_summary":
        return (
            f"{startup.name} is a {startup.stage}-stage {startup.domain} startup "
            f"based in {startup.location}. We are applying for the {grant.title} "
            f"({grant.source}) to accelerate our product development and market expansion. "
            f"Our solution addresses a critical gap in the {startup.domain} space: "
            f"{startup.description[:300]}"
        )
    elif section == "problem_statement":
        return (
            f"The {startup.domain} sector faces significant challenges that {startup.name} "
            f"is uniquely positioned to solve. {startup.description}"
        )
    elif section == "solution":
        return (
            f"{startup.name} has developed an innovative approach to address these challenges. "
            f"{startup.description} "
            f"With support from {grant.title}, we will scale this solution to reach more users."
        )
    elif section == "impact":
        return (
            f"With the {grant.funding_amount} from {grant.title}, {startup.name} "
            f"will deliver measurable impact in {startup.domain}. "
            f"We project significant growth in user adoption, revenue, and job creation "
            f"within 18 months of funding."
        )
    elif section == "budget":
        return (
            f"The requested funding of {grant.funding_amount} will be allocated as follows: "
            f"40% product development, 30% market expansion, 20% team hiring, "
            f"10% operations. Current team size: {startup.team_size or 'Early stage'}."
        )
    else:  # full
        return f"""## Grant Application: {grant.title}

### 1. Executive Summary
{startup.name} is a {startup.stage}-stage {startup.domain} startup based in {startup.location}. We are applying for the {grant.title} ({grant.source}) to accelerate our mission.

### 2. Problem Statement
{startup.description}

### 3. Proposed Solution
Our team has developed a unique approach that leverages the latest advances in {startup.domain} to deliver measurable outcomes.

### 4. Expected Impact & Outcomes
With the {grant.funding_amount} from this grant, we will scale our solution, create jobs, and deliver meaningful impact in {startup.domain}.

### 5. Budget Overview
Requested: {grant.funding_amount}
- 40% Product Development
- 30% Market Expansion
- 20% Talent & HR
- 10% Operations

---
*Note: Configure IBM_API_KEY in .env for AI-generated proposals using IBM Granite.*
"""


def answer_eligibility_question(
    grant: GrantOpportunity,
    startup: StartupProfile,
    question: str,
) -> str:
    """
    Answer a specific eligibility or compliance question using Granite.
    """
    prompt = (
        f"You are a grant eligibility advisor. Answer the following question "
        f"based on the grant details provided. Be concise and accurate.\n\n"
        f"Grant: {grant.title}\n"
        f"Eligibility Criteria: {grant.eligibility}\n"
        f"Startup: {startup.name} — {startup.domain}, {startup.stage} stage, {startup.location}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    result = _call_granite(prompt)
    if result:
        return result

    return (
        f"Based on the eligibility criteria for {grant.title}: '{grant.eligibility}', "
        f"your startup ({startup.name} — {startup.stage} stage, {startup.domain}, "
        f"{startup.location}) should review these requirements carefully. "
        f"Please consult the official grant portal at {grant.url} for definitive guidance."
    )
