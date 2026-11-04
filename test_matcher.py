"""
test_matcher.py — Unit tests for the grant matching engine (no IBM credentials required).
Run: python -m pytest test_matcher.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from backend.models import StartupProfile
from backend.grant_database import get_all_grants
from backend.matcher import rank_grants, score_grant


AGRI_INDIA_SEED = StartupProfile(
    name="FarmSense",
    domain="AgriTech",
    stage="Seed",
    location="India",
    description=(
        "FarmSense provides IoT-based soil monitoring solutions for smallholder "
        "farmers in India, enabling precision farming through real-time data."
    ),
)

FINTECH_USA = StartupProfile(
    name="PayFlow",
    domain="FinTech",
    stage="Series-A",
    location="USA",
    description=(
        "PayFlow is a B2B payment orchestration platform reducing cross-border "
        "transaction costs for SMEs using AI-driven FX optimization."
    ),
)

CLEANTECH_EU = StartupProfile(
    name="SolarNow",
    domain="CleanEnergy",
    stage="Pre-Seed",
    location="Germany",
    description=(
        "SolarNow develops modular solar kits for off-grid communities in "
        "Sub-Saharan Africa, distributed via mobile-money microfinance."
    ),
)


def test_grants_loaded():
    grants = get_all_grants()
    assert len(grants) >= 10, "Should load at least 10 seed grants"


def test_rank_returns_sorted():
    grants = get_all_grants()
    ranked = rank_grants(AGRI_INDIA_SEED, grants, max_results=10)
    scores = [g.match_score for g in ranked]
    assert scores == sorted(scores, reverse=True), "Results should be sorted by match_score desc"


def test_agri_india_top_grants():
    grants = get_all_grants()
    ranked = rank_grants(AGRI_INDIA_SEED, grants, max_results=5)
    titles = [g.title for g in ranked]
    # India AgriTech seed should match Startup India / BIRAC / AgriUdaan
    india_matches = [t for t in titles if any(kw in t for kw in ["Startup India", "BIRAC", "AgriUdaan", "NIDHI", "TIDE", "Atal"])]
    assert len(india_matches) >= 1, f"Expected India-specific grants in top-5, got: {titles}"


def test_fintech_usa():
    grants = get_all_grants()
    ranked = rank_grants(FINTECH_USA, grants, max_results=5)
    assert len(ranked) >= 1


def test_cleantech_eu():
    grants = get_all_grants()
    ranked = rank_grants(CLEANTECH_EU, grants, max_results=5)
    assert len(ranked) >= 1


def test_score_between_0_and_1():
    grants = get_all_grants()
    for g in grants:
        score, _ = score_grant(AGRI_INDIA_SEED, g)
        assert 0.0 <= score <= 1.0, f"Score out of range for {g.id}: {score}"


def test_max_results_respected():
    grants = get_all_grants()
    ranked = rank_grants(AGRI_INDIA_SEED, grants, max_results=3)
    assert len(ranked) <= 3


def test_min_score_filter():
    grants = get_all_grants()
    ranked = rank_grants(AGRI_INDIA_SEED, grants, max_results=50, min_score=0.5)
    for g in ranked:
        assert g.match_score >= 0.5, f"Grant below min_score: {g.id} = {g.match_score}"


def test_match_reasons_populated():
    grants = get_all_grants()
    ranked = rank_grants(AGRI_INDIA_SEED, grants, max_results=10)
    top = ranked[0]
    # At least one reason should be present for the top match
    assert len(top.match_reasons) >= 1, "Top match should have match reasons"


if __name__ == "__main__":
    import traceback
    tests = [
        test_grants_loaded,
        test_rank_returns_sorted,
        test_agri_india_top_grants,
        test_fintech_usa,
        test_cleantech_eu,
        test_score_between_0_and_1,
        test_max_results_respected,
        test_min_score_filter,
        test_match_reasons_populated,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            traceback.print_exc()
    print(f"\n{passed}/{len(tests)} tests passed")
