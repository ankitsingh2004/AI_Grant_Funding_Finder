"""
app.py — Streamlit frontend for AI Grant & Funding Finder for Startups
Powered by IBM Granite AI
"""
import streamlit as st
import time
from backend.grant_database import get_all_grants
from backend.matcher import rank_grants
from backend.models import StartupProfile
from backend.granite_service import (
    generate_startup_summary,
    generate_proposal_section,
    answer_eligibility_question,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Grant Finder — IBM Granite",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Full custom CSS + animations
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global reset ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp { background: #0a0e1a; }

/* ── Animated gradient hero banner ────────────────────────────────── */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(15,98,254,0.4); }
    50%       { box-shadow: 0 0 0 12px rgba(15,98,254,0); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes floatUp {
    0%   { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.5); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes borderGlow {
    0%, 100% { border-color: #0f62fe; box-shadow: 0 0 8px rgba(15,98,254,0.3); }
    50%       { border-color: #a56eff; box-shadow: 0 0 20px rgba(165,110,255,0.5); }
}

/* ── Hero Banner ───────────────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(-45deg, #0a0e1a, #0f62fe, #0043ce, #6929c4, #0a0e1a);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    padding: 3rem 2.5rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(15,98,254,0.15) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(165,110,255,0.1) 0%, transparent 50%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4rem; font-weight: 800; color: #ffffff;
    letter-spacing: -0.5px; margin: 0 0 0.5rem;
    animation: fadeSlideDown 0.8s ease both;
    text-shadow: 0 2px 20px rgba(0,0,0,0.4);
}
.hero-subtitle {
    font-size: 1rem; color: rgba(255,255,255,0.75);
    margin: 0; animation: fadeSlideDown 0.8s 0.15s ease both;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #fff; border-radius: 20px;
    padding: 4px 14px; font-size: 0.75rem; font-weight: 600;
    margin-bottom: 1rem;
    animation: fadeSlideDown 0.8s 0s ease both;
    backdrop-filter: blur(6px);
}
.hero-stats {
    display: flex; gap: 2rem; margin-top: 1.8rem; flex-wrap: wrap;
    animation: fadeSlideUp 0.8s 0.3s ease both;
}
.hero-stat {
    text-align: center;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px; padding: 0.7rem 1.4rem;
    backdrop-filter: blur(8px);
    transition: transform 0.2s, background 0.2s;
}
.hero-stat:hover { transform: translateY(-3px); background: rgba(255,255,255,0.13); }
.hero-stat .num { font-size: 1.6rem; font-weight: 800; color: #fff; display: block; }
.hero-stat .lbl { font-size: 0.72rem; color: rgba(255,255,255,0.6); font-weight: 500; }

/* ── Sidebar ───────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0d1120 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

/* All text nodes inside sidebar — labels, captions, markdown */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stTextArea label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSlider [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption p {
    color: #e2e8f0 !important;
}

/* Input / select / textarea fields */
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stTextArea textarea,
[data-testid="stSidebar"] .stNumberInput input {
    background: #1a2035 !important;
    border: 1px solid rgba(15,98,254,0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stSidebar"] .stTextInput input::placeholder,
[data-testid="stSidebar"] .stTextArea textarea::placeholder {
    color: #6b7280 !important;
}
[data-testid="stSidebar"] .stTextInput input:focus,
[data-testid="stSidebar"] .stTextArea textarea:focus {
    border-color: #0f62fe !important;
    box-shadow: 0 0 0 3px rgba(15,98,254,0.2) !important;
}

/* Selectbox dropdown */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #1a2035 !important;
    border: 1px solid rgba(15,98,254,0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #ffffff !important;
}

/* Slider value text */
[data-testid="stSidebar"] [data-testid="stSlider"] p,
[data-testid="stSidebar"] [data-testid="stSlider"] span {
    color: #e2e8f0 !important;
}

/* Divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* Section heading bold text */
[data-testid="stSidebar"] strong {
    color: #ffffff !important;
}

.sidebar-header {
    background: linear-gradient(135deg, #0f62fe, #6929c4);
    border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 1.2rem;
    animation: fadeSlideDown 0.6s ease both;
}
.sidebar-header h2 { margin: 0; color: #fff !important; font-size: 1.1rem; font-weight: 700; }
.sidebar-header p  { margin: 0.2rem 0 0; color: rgba(255,255,255,0.7) !important; font-size: 0.8rem; }

/* ── Tab styling ───────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1120 !important;
    border-radius: 12px; padding: 4px; gap: 4px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #8892a4 !important;
    border-radius: 8px; font-weight: 500; font-size: 0.88rem;
    padding: 0.5rem 1.2rem; transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0f62fe, #6929c4) !important;
    color: #fff !important; font-weight: 600;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent; padding-top: 1.5rem;
}

/* ── Grant cards ───────────────────────────────────────────────────── */
.grant-card {
    background: linear-gradient(135deg, #0d1120 0%, #111827 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 4px solid #0f62fe;
    border-radius: 14px; padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: transform 0.25s cubic-bezier(.25,.46,.45,.94),
                box-shadow 0.25s, border-color 0.25s;
    animation: floatUp 0.5s ease both;
    position: relative; overflow: hidden;
}
.grant-card::after {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(15,98,254,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.grant-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(15,98,254,0.2);
    border-left-color: #a56eff;
}
.grant-card-title {
    font-size: 1.05rem; font-weight: 700; color: #e2e8f0; margin: 0 0 0.4rem;
}
.grant-card-meta {
    font-size: 0.8rem; color: #6b7280; margin-bottom: 0.7rem; display: flex; gap: 1rem; flex-wrap: wrap;
}
.grant-card-meta span { display: flex; align-items: center; gap: 4px; }

/* ── Badges & tags ────────────────────────────────────────────────── */
.score-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: linear-gradient(135deg, #0f62fe, #6929c4);
    color: #fff; padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    box-shadow: 0 2px 8px rgba(15,98,254,0.4);
    animation: pulse 2s infinite;
}
.score-bar-wrap { margin: 0.5rem 0; }
.score-bar-bg {
    background: rgba(255,255,255,0.06); border-radius: 99px;
    height: 6px; width: 100%; overflow: hidden;
}
.score-bar-fill {
    height: 100%; border-radius: 99px;
    background: linear-gradient(90deg, #0f62fe, #a56eff);
    transition: width 1s cubic-bezier(.25,.46,.45,.94);
}
.tag {
    display: inline-block; background: rgba(15,98,254,0.15);
    border: 1px solid rgba(15,98,254,0.3); color: #60a5fa;
    padding: 2px 10px; border-radius: 20px; font-size: 0.72rem;
    font-weight: 500; margin: 2px; transition: background 0.2s;
}
.tag:hover { background: rgba(15,98,254,0.3); }
.reason-tag {
    display: inline-block; background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3); color: #34d399;
    padding: 2px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 500; margin: 2px;
}
.location-tag {
    display: inline-block; background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.3); color: #fbbf24;
    padding: 2px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 500; margin: 2px;
}

/* ── Stats row ────────────────────────────────────────────────────── */
.stat-card {
    background: linear-gradient(135deg, #0d1120, #111827);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 1.2rem 1.4rem; text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    animation: floatUp 0.5s ease both;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(15,98,254,0.15); }
.stat-num { font-size: 2rem; font-weight: 800; color: #60a5fa; display: block; }
.stat-lbl { font-size: 0.78rem; color: #6b7280; font-weight: 500; margin-top: 2px; }

/* ── Summary box ──────────────────────────────────────────────────── */
.summary-box {
    background: linear-gradient(135deg, rgba(15,98,254,0.1), rgba(105,41,196,0.1));
    border: 1px solid rgba(15,98,254,0.25);
    border-radius: 14px; padding: 1.4rem 1.6rem;
    margin-bottom: 1.5rem;
    animation: borderGlow 3s ease infinite;
}
.summary-box .label { font-size: 0.75rem; font-weight: 700; color: #60a5fa; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.4rem; }
.summary-box .text  { color: #c4cdd6; font-size: 0.95rem; line-height: 1.6; }

/* ── Proposal output ─────────────────────────────────────────────── */
.proposal-output {
    background: #0d1120; border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px; padding: 1.6rem;
    color: #c4cdd6; line-height: 1.8; font-size: 0.93rem;
    animation: fadeSlideUp 0.5s ease both;
}
.proposal-output h3 { color: #60a5fa; font-size: 1rem; margin-top: 1rem; }

/* ── Section divider ──────────────────────────────────────────────── */
.section-title {
    font-size: 1.25rem; font-weight: 700; color: #e2e8f0;
    margin: 1.5rem 0 1rem; display: flex; align-items: center; gap: 10px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(15,98,254,0.4), transparent);
}

/* ── Expander ─────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #0d1120 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: #8892a4 !important; font-size: 0.85rem !important;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0f62fe, #6929c4) !important;
    border: none !important; border-radius: 10px !important;
    color: #fff !important; font-weight: 600 !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 15px rgba(15,98,254,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: 0.92 !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(15,98,254,0.45) !important;
}
.stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #c4cdd6 !important; border-radius: 10px !important;
    transition: background 0.2s, transform 0.2s !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(255,255,255,0.1) !important; transform: translateY(-1px) !important;
}

/* ── Inputs (main area) ───────────────────────────────────────────── */
.stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
    background: #0d1120 !important; border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e2e8f0 !important; border-radius: 10px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #0f62fe !important;
    box-shadow: 0 0 0 3px rgba(15,98,254,0.15) !important;
}

/* ── Slider ───────────────────────────────────────────────────────── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(135deg, #0f62fe, #6929c4) !important;
    border: none !important;
}

/* ── Spinner ──────────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: #0f62fe !important; }

/* ── Alerts ───────────────────────────────────────────────────────── */
.stAlert { border-radius: 10px !important; }

/* ── Empty state ──────────────────────────────────────────────────── */
.empty-state {
    text-align: center; padding: 4rem 2rem;
    color: #4b5563; animation: fadeSlideUp 0.6s ease both;
}
.empty-state .icon { font-size: 4rem; margin-bottom: 1rem; display: block; }
.empty-state h3 { color: #6b7280; font-size: 1.1rem; margin-bottom: 0.5rem; }
.empty-state p  { font-size: 0.88rem; max-width: 380px; margin: 0 auto; }

/* ── How it works cards ───────────────────────────────────────────── */
.how-card {
    background: linear-gradient(135deg, #0d1120, #111827);
    border: 1px solid rgba(255,255,255,0.07); border-radius: 14px;
    padding: 1.4rem; text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    animation: floatUp 0.5s ease both;
}
.how-card:hover { transform: translateY(-4px); box-shadow: 0 10px 35px rgba(15,98,254,0.15); }
.how-card .step-num {
    width: 44px; height: 44px; border-radius: 50%;
    background: linear-gradient(135deg, #0f62fe, #6929c4);
    color: #fff; font-weight: 800; font-size: 1.1rem;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 0.8rem; box-shadow: 0 4px 15px rgba(15,98,254,0.4);
}
.how-card h4 { color: #e2e8f0; margin: 0 0 0.4rem; font-size: 0.95rem; }
.how-card p  { color: #6b7280; font-size: 0.82rem; margin: 0; line-height: 1.5; }

/* ── Footer ───────────────────────────────────────────────────────── */
.app-footer {
    text-align: center; margin-top: 4rem; padding: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    color: #374151; font-size: 0.78rem;
}
.app-footer span { color: #0f62fe; font-weight: 600; }

/* ── Scrollbar ────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #0f62fe; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
  <div class="hero-badge">🏆 AICTE Hackathon — Problem Statement #18</div>
  <div class="hero-title">💡 AI Grant &amp; Funding Finder</div>
  <div class="hero-subtitle">Discover personalised grants &amp; auto-generate proposals — Powered by <strong>IBM Granite AI</strong></div>
  <div class="hero-stats">
    <div class="hero-stat"><span class="num">22+</span><span class="lbl">Curated Grants</span></div>
    <div class="hero-stat"><span class="num">4</span><span class="lbl">Regions Covered</span></div>
    <div class="hero-stat"><span class="num">AI</span><span class="lbl">IBM Granite Powered</span></div>
    <div class="hero-stat"><span class="num">Free</span><span class="lbl">IBM Cloud Lite</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
      <h2>🚀 Startup Profile</h2>
      <p>Tell us about your startup to find the best grants</p>
    </div>
    """, unsafe_allow_html=True)

    startup_name = st.text_input("Startup Name", placeholder="e.g. FarmSense AI")

    domain = st.selectbox("Industry Domain", [
        "AgriTech", "HealthTech", "EdTech", "FinTech",
        "CleanEnergy", "AI/ML", "Cybersecurity", "DeepTech",
        "SaaS", "Blockchain", "IoT", "Biotech", "MedTech",
        "FoodTech", "Robotics", "Hardware",
    ])

    stage = st.selectbox("Startup Stage", [
        "Idea", "Pre-Seed", "Seed", "Series-A", "Growth"
    ])

    location = st.text_input("Location", placeholder="e.g. India, USA, UK")

    description = st.text_area(
        "Startup Description",
        placeholder="Describe what your startup does in 1–2 sentences...",
        height=110,
    )

    team_size = st.number_input("Team Size", min_value=1, max_value=10000, value=5, step=1)

    keywords_input = st.text_input(
        "Keywords (comma-separated)",
        placeholder="e.g. IoT, precision farming, rural"
    )

    st.divider()
    st.markdown("**⚙️ Search Settings**")
    max_results = st.slider("Max Results", 1, 20, 10)
    min_score   = st.slider("Min Match Score", 0.0, 1.0, 0.1, step=0.05,
                             help="Only show grants above this relevance score")

    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔍  Find Matching Grants", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_search, tab_browse, tab_qa = st.tabs([
    "🎯  Personalised Matches",
    "📋  Browse All Grants",
    "❓  Eligibility Q&A",
])

# ---------------------------------------------------------------------------
# Helper: build a startup object from sidebar values
# ---------------------------------------------------------------------------
def build_startup():
    return StartupProfile(
        name=startup_name,
        domain=domain,
        stage=stage,
        location=location,
        description=description,
        team_size=int(team_size),
        keywords=[k.strip() for k in keywords_input.split(",") if k.strip()],
    )

# ---------------------------------------------------------------------------
# Helper: render one grant card
# ---------------------------------------------------------------------------
def render_grant_card(grant, show_score=True, key_prefix="", delay_index=0):
    score_pct = int(grant.match_score * 100)
    score_html = f'<span class="score-badge">⚡ {score_pct}% Match</span>' if show_score and grant.match_score > 0 else ""

    domain_tags_html   = " ".join(f'<span class="tag">{t}</span>' for t in grant.domain_tags[:4])
    location_tags_html = " ".join(f'<span class="location-tag">📍 {t}</span>' for t in grant.location_tags[:3])
    reasons_html       = " ".join(f'<span class="reason-tag">✓ {r}</span>' for r in grant.match_reasons)

    bar_width = score_pct if show_score else 0

    st.markdown(f"""
    <div class="grant-card" style="animation-delay:{delay_index * 0.08}s">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem;">
        <div class="grant-card-title">{grant.title}</div>
        {score_html}
      </div>
      <div class="grant-card-meta">
        <span>🏛️ {grant.source}</span>
        <span>💰 {grant.funding_amount}</span>
        <span>📅 {grant.deadline}</span>
      </div>
      {"<div class='score-bar-wrap'><div class='score-bar-bg'><div class='score-bar-fill' style='width:" + str(bar_width) + "%'></div></div></div>" if show_score and bar_width > 0 else ""}
      <div style="margin-top:0.5rem">{domain_tags_html} {location_tags_html}</div>
      {"<div style='margin-top:0.4rem'>" + reasons_html + "</div>" if reasons_html else ""}
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"📄 Details & AI Proposal — {grant.title[:55]}"):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown("**📝 About this Grant**")
            st.markdown(f"<p style='color:#9ca3af;font-size:0.9rem;line-height:1.6'>{grant.description}</p>", unsafe_allow_html=True)
            st.markdown("**✅ Eligibility**")
            st.markdown(f"<p style='color:#9ca3af;font-size:0.9rem;line-height:1.6'>{grant.eligibility}</p>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style='background:#111827;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:1rem;'>
              <div style='color:#6b7280;font-size:0.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.3rem'>FUNDING</div>
              <div style='color:#60a5fa;font-weight:700;font-size:0.95rem;margin-bottom:1rem'>{grant.funding_amount}</div>
              <div style='color:#6b7280;font-size:0.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.3rem'>DEADLINE</div>
              <div style='color:#fbbf24;font-weight:600;font-size:0.9rem;margin-bottom:1rem'>{grant.deadline}</div>
              <div style='color:#6b7280;font-size:0.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.3rem'>STAGE</div>
              <div style='margin-bottom:1rem'>{"".join(f"<span class='tag'>{s}</span>" for s in grant.stage_tags)}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"[🔗 Official Grant Portal]({grant.url})", unsafe_allow_html=False)

        st.divider()
        st.markdown("**🤖 AI Proposal Generator (IBM Granite)**")
        pcol1, pcol2 = st.columns([2, 1])
        with pcol1:
            section = st.selectbox(
                "Choose section to generate",
                ["full", "executive_summary", "problem_statement", "solution", "impact", "budget"],
                key=f"{key_prefix}_{grant.id}_section",
                format_func=lambda x: {
                    "full": "📄 Full Proposal",
                    "executive_summary": "📌 Executive Summary",
                    "problem_statement": "🔍 Problem Statement",
                    "solution": "💡 Solution",
                    "impact": "🌍 Impact & Outcomes",
                    "budget": "💰 Budget Justification",
                }.get(x, x)
            )
        with pcol2:
            gen_btn = st.button("✨ Generate", key=f"{key_prefix}_{grant.id}_gen", type="primary")

        if gen_btn:
            if not startup_name or not description or not location:
                st.warning("⚠️ Please fill in Startup Name, Description, and Location in the sidebar first.")
            else:
                with st.spinner("🧠 IBM Granite is crafting your proposal..."):
                    proposal = generate_proposal_section(
                        grant=grant, startup=build_startup(), section=section
                    )
                st.markdown(f"""
                <div class="proposal-output">
                {proposal.content.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                st.caption(f"📝 {proposal.word_count} words · ⚠️ {proposal.disclaimer}")

# ---------------------------------------------------------------------------
# TAB 1 — Personalised Matches
# ---------------------------------------------------------------------------
with tab_search:
    if search_btn:
        if not startup_name or not description or not location:
            st.error("⚠️ Please fill in Startup Name, Description, and Location in the sidebar.")
        else:
            progress_bar = st.progress(0, text="Initialising search...")
            time.sleep(0.1); progress_bar.progress(20, text="Loading grant database...")
            all_grants = get_all_grants()
            time.sleep(0.1); progress_bar.progress(50, text="Scoring grants against your profile...")
            ranked = rank_grants(build_startup(), all_grants, max_results=max_results, min_score=min_score)
            time.sleep(0.1); progress_bar.progress(80, text="Generating your startup summary with IBM Granite...")
            summary = generate_startup_summary(build_startup())
            time.sleep(0.1); progress_bar.progress(100, text="Done!")
            time.sleep(0.4); progress_bar.empty()

            # Stats row
            top_score = f"{int(ranked[0].match_score * 100)}%" if ranked else "—"
            c1, c2, c3, c4 = st.columns(4)
            for col, num, lbl in zip(
                [c1, c2, c3, c4],
                [len(ranked), top_score, domain, stage],
                ["Grants Found", "Top Match Score", "Your Domain", "Your Stage"]
            ):
                col.markdown(f"""
                <div class="stat-card">
                  <span class="stat-num">{num}</span>
                  <div class="stat-lbl">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Startup summary
            st.markdown(f"""
            <div class="summary-box">
              <div class="label">🤖 IBM Granite — Startup Summary</div>
              <div class="text">{summary}</div>
            </div>
            """, unsafe_allow_html=True)

            # Results
            st.markdown(f'<div class="section-title">🎯 Matching Grants ({len(ranked)} found)</div>', unsafe_allow_html=True)

            if not ranked:
                st.markdown("""
                <div class="empty-state">
                  <span class="icon">🔍</span>
                  <h3>No matches found</h3>
                  <p>Try lowering the Min Match Score or adjusting your domain, stage, or location.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for i, grant in enumerate(ranked):
                    render_grant_card(grant, show_score=True, key_prefix="search", delay_index=i)

    else:
        # Landing / empty state
        st.markdown("""
        <div class="empty-state" style="padding:2rem 0 1rem;">
          <span class="icon">👈</span>
          <h3>Fill your Startup Profile</h3>
          <p>Enter your startup details in the sidebar and click <strong style="color:#60a5fa">Find Matching Grants</strong> to get started.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">✨ How It Works</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        steps = [
            ("1", "Fill Profile", "Enter your startup name, domain, stage, location & description in the sidebar."),
            ("2", "AI Matching", "Our engine scores all 22+ grants using domain, stage, location & keyword signals."),
            ("3", "Ranked Results", "Grants are ranked by relevance score with clear match reasons shown."),
            ("4", "Generate Proposals", "IBM Granite AI writes a tailored application draft for any grant — instantly."),
        ]
        for col, (num, title, desc) in zip(cols, steps):
            col.markdown(f"""
            <div class="how-card">
              <div class="step-num">{num}</div>
              <h4>{title}</h4>
              <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 2 — Browse All Grants
# ---------------------------------------------------------------------------
with tab_browse:
    st.markdown('<div class="section-title">📋 All Available Grants</div>', unsafe_allow_html=True)

    all_grants_browse = get_all_grants()

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filter_domain = st.selectbox("🔖 Filter by Domain", ["All"] + [
            "AgriTech", "HealthTech", "EdTech", "FinTech", "CleanEnergy",
            "AI/ML", "Cybersecurity", "DeepTech", "SaaS", "Blockchain", "IoT"
        ], key="browse_domain")
    with fc2:
        filter_stage = st.selectbox("📈 Filter by Stage",
            ["All", "Idea", "Pre-Seed", "Seed", "Series-A", "Growth"], key="browse_stage")
    with fc3:
        filter_location = st.selectbox("🌍 Filter by Location",
            ["All", "India", "USA", "Europe", "UK", "Global"], key="browse_location")

    filtered = all_grants_browse
    if filter_domain != "All":
        dl = filter_domain.lower()
        filtered = [g for g in filtered if any(dl in t.lower() for t in g.domain_tags) or "all" in g.domain_tags]
    if filter_stage != "All":
        filtered = [g for g in filtered if any(filter_stage.lower() in t.lower() for t in g.stage_tags)]
    if filter_location != "All":
        ll = filter_location.lower()
        filtered = [g for g in filtered if any(ll in t.lower() or "global" in t.lower() for t in g.location_tags)]

    st.markdown(f"<p style='color:#6b7280;font-size:0.85rem;margin-bottom:1rem'>Showing <strong style='color:#60a5fa'>{len(filtered)}</strong> of {len(all_grants_browse)} grants</p>", unsafe_allow_html=True)

    if not filtered:
        st.markdown("""
        <div class="empty-state">
          <span class="icon">📭</span>
          <h3>No grants match these filters</h3>
          <p>Try changing the domain, stage, or location filter.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, grant in enumerate(filtered):
            render_grant_card(grant, show_score=False, key_prefix="browse", delay_index=i)

# ---------------------------------------------------------------------------
# TAB 3 — Eligibility Q&A
# ---------------------------------------------------------------------------
with tab_qa:
    st.markdown('<div class="section-title">❓ Eligibility Q&A — Powered by IBM Granite</div>', unsafe_allow_html=True)

    st.markdown("""
    <p style='color:#6b7280;font-size:0.88rem;margin-bottom:1.5rem'>
    Select any grant and ask a natural-language question about its eligibility criteria.
    IBM Granite AI will analyse your startup profile and the grant requirements to give you a direct answer.
    </p>
    """, unsafe_allow_html=True)

    all_grants_qa = get_all_grants()
    grant_options = {g.title: g for g in all_grants_qa}

    qc1, qc2 = st.columns([2, 1])
    with qc1:
        selected_title = st.selectbox("🏛️ Select a Grant", list(grant_options.keys()), key="qa_grant")
    with qc2:
        st.markdown("<br>", unsafe_allow_html=True)

    selected_grant = grant_options[selected_title]

    st.markdown(f"""
    <div style='background:#0d1120;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:1rem 1.2rem;margin-bottom:1.2rem;'>
      <div style='color:#6b7280;font-size:0.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.4rem'>ELIGIBILITY CRITERIA</div>
      <div style='color:#9ca3af;font-size:0.88rem;line-height:1.6'>{selected_grant.eligibility}</div>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "💬 Your Question",
        placeholder="e.g. Are we eligible if our startup was incorporated 3 years ago?",
        key="qa_question"
    )

    ask_btn = st.button("🧠 Ask IBM Granite", type="primary", key="qa_ask")

    if ask_btn:
        if not question.strip():
            st.warning("Please enter a question.")
        elif not startup_name or not description or not location:
            st.warning("Fill in your startup profile in the sidebar first.")
        else:
            with st.spinner("🧠 IBM Granite is analysing eligibility..."):
                answer = answer_eligibility_question(
                    grant=selected_grant,
                    startup=build_startup(),
                    question=question,
                )
            st.markdown(f"""
            <div class="summary-box" style="margin-top:1rem">
              <div class="label">🤖 IBM Granite — Answer</div>
              <div class="text">{answer}</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("⚠️ AI-generated — always verify on the official grant portal before submitting.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
<div class="app-footer">
  Made with <span>IBM Bob</span> &nbsp;·&nbsp; Powered by <span>IBM Granite AI</span>
  &nbsp;·&nbsp; AICTE Hackathon Problem Statement #18
  &nbsp;·&nbsp; IBM Cloud Lite (Free Tier)
</div>
""", unsafe_allow_html=True)
