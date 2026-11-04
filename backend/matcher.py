"""
matcher.py — Personalized grant matching engine.

Uses keyword overlap + semantic similarity heuristics to score each grant
against a startup profile and return a ranked, filtered list.
No external ML model is required at runtime — scoring is deterministic
and fast, making it reliable even without a GPU.
"""
from __future__ import annotations
import re
from typing import List, Tuple
from backend.models import GrantOpportunity, StartupProfile


# ---------------------------------------------------------------------------
# Domain synonym map — normalises user input to canonical tags
# ---------------------------------------------------------------------------
DOMAIN_SYNONYMS: dict[str, List[str]] = {
    "healthtech": ["health", "medtech", "medical", "health tech", "healthcare", "biotech", "pharma"],
    "edtech": ["education", "ed tech", "e-learning", "learning", "school", "university"],
    "agritech": ["agriculture", "agri", "farm", "farming", "food", "foodtech", "rural"],
    "fintech": ["finance", "financial", "banking", "payments", "lending", "insurance"],
    "cleanenergy": ["clean", "renewable", "solar", "wind", "energy", "climate", "green", "sustainability"],
    "ai/ml": ["artificial intelligence", "machine learning", "deep learning", "nlp", "computer vision", "data science"],
    "cybersecurity": ["security", "cyber", "infosec", "privacy", "encryption"],
    "deeptech": ["hardware", "robotics", "quantum", "space", "semiconductor", "biotech", "advanced manufacturing"],
    "saas": ["software", "platform", "b2b", "enterprise", "cloud"],
    "blockchain": ["crypto", "web3", "nft", "defi", "distributed ledger"],
    "iot": ["internet of things", "connected devices", "smart devices", "embedded"],
}

STAGE_ORDER = ["Idea", "Pre-Seed", "Seed", "Series-A", "Growth"]


def _normalize(text: str) -> str:
    return text.lower().strip()


def _domain_score(startup_domain: str, grant_domain_tags: List[str]) -> float:
    """
    Returns a 0–1 score based on domain relevance.
    1.0 = exact tag match, 0.7 = synonym match, 0.2 = "all" catchall, 0.0 = no match.
    """
    nd = _normalize(startup_domain)
    # Direct match
    for tag in grant_domain_tags:
        if _normalize(tag) == nd:
            return 1.0
        if _normalize(tag) == "all":
            pass  # handled below

    # Synonym-based match
    canonical = None
    for canon, synonyms in DOMAIN_SYNONYMS.items():
        if nd == canon or any(syn in nd for syn in synonyms):
            canonical = canon
            break

    if canonical:
        for tag in grant_domain_tags:
            if _normalize(tag) == canonical:
                return 1.0
            # check cross-synonym
            for syn in DOMAIN_SYNONYMS.get(canonical, []):
                if syn in _normalize(tag):
                    return 0.8

    # Catchall
    if any(_normalize(t) == "all" for t in grant_domain_tags):
        return 0.3

    return 0.0


def _stage_score(startup_stage: str, grant_stage_tags: List[str]) -> float:
    """
    Returns a 0–1 score based on stage overlap.
    """
    if not grant_stage_tags:
        return 0.5  # unspecified → neutral

    ns = _normalize(startup_stage)
    # exact
    for tag in grant_stage_tags:
        if _normalize(tag) == ns:
            return 1.0

    # adjacent stage (one step away)
    if startup_stage in STAGE_ORDER:
        idx = STAGE_ORDER.index(startup_stage)
        neighbours = []
        if idx > 0:
            neighbours.append(_normalize(STAGE_ORDER[idx - 1]))
        if idx < len(STAGE_ORDER) - 1:
            neighbours.append(_normalize(STAGE_ORDER[idx + 1]))
        for tag in grant_stage_tags:
            if _normalize(tag) in neighbours:
                return 0.5

    return 0.0


def _location_score(startup_location: str, grant_location_tags: List[str]) -> float:
    """
    Returns a 0–1 score based on location relevance.
    """
    if not grant_location_tags:
        return 0.5

    nl = _normalize(startup_location)

    for tag in grant_location_tags:
        nt = _normalize(tag)
        if nt == "global":
            return 0.6
        if nt in nl or nl in nt:
            return 1.0

    # Country → region mapping
    region_map = {
        "india": ["south asia", "asia"],
        "usa": ["north america", "americas"],
        "uk": ["europe"],
        "germany": ["europe", "eu"],
        "france": ["europe", "eu"],
        "nigeria": ["africa"],
        "kenya": ["africa"],
        "brazil": ["latin america", "americas"],
    }
    country = nl.split(",")[0].strip()
    regions = region_map.get(country, [])
    for tag in grant_location_tags:
        if _normalize(tag) in regions:
            return 0.7

    return 0.0


def _keyword_overlap_score(startup: StartupProfile, grant: GrantOpportunity) -> float:
    """
    Simple bag-of-words overlap between startup description + keywords
    and grant title + description.
    """
    startup_text = " ".join([
        startup.description,
        startup.domain,
        startup.name,
        " ".join(startup.keywords or []),
    ]).lower()
    grant_text = " ".join([grant.title, grant.description, grant.eligibility]).lower()

    # tokenise
    sw = set(re.findall(r"\b[a-z]{4,}\b", startup_text))
    gw = set(re.findall(r"\b[a-z]{4,}\b", grant_text))

    if not sw or not gw:
        return 0.0

    overlap = len(sw & gw)
    return min(overlap / 10, 1.0)  # cap at 1.0; 10+ common words = full score


def score_grant(startup: StartupProfile, grant: GrantOpportunity) -> Tuple[float, List[str]]:
    """
    Returns (composite_score 0–1, list_of_match_reasons).
    Weights: domain 40%, stage 25%, location 20%, keyword 15%.
    """
    reasons: List[str] = []

    d_score = _domain_score(startup.domain, grant.domain_tags)
    s_score = _stage_score(startup.stage, grant.stage_tags)
    l_score = _location_score(startup.location, grant.location_tags)
    k_score = _keyword_overlap_score(startup, grant)

    composite = (d_score * 0.40) + (s_score * 0.25) + (l_score * 0.20) + (k_score * 0.15)

    if d_score >= 0.8:
        reasons.append(f"Strong domain match: {startup.domain}")
    elif d_score >= 0.3:
        reasons.append(f"Partial domain match: {startup.domain}")

    if s_score >= 0.9:
        reasons.append(f"Exact stage match: {startup.stage}")
    elif s_score >= 0.5:
        reasons.append(f"Adjacent stage ({startup.stage}) also eligible")

    if l_score >= 0.9:
        reasons.append(f"Location eligible: {startup.location}")
    elif l_score >= 0.5:
        reasons.append(f"Region eligible for: {startup.location}")

    if k_score >= 0.3:
        reasons.append("Strong keyword overlap with grant description")

    return round(composite, 4), reasons


def rank_grants(
    startup: StartupProfile,
    grants: List[GrantOpportunity],
    max_results: int = 10,
    min_score: float = 0.0,
) -> List[GrantOpportunity]:
    """
    Score all grants against the startup profile, filter by min_score,
    sort descending, return top max_results.
    """
    scored: List[GrantOpportunity] = []
    for grant in grants:
        score, reasons = score_grant(startup, grant)
        if score >= min_score:
            g = grant.model_copy(
                update={"match_score": score, "match_reasons": reasons}
            )
            scored.append(g)

    scored.sort(key=lambda x: x.match_score, reverse=True)
    return scored[:max_results]
