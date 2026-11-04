"""
grant_database.py — Curated, structured grant/funding database.

In production this module would be augmented by live scrapers and RSS feeds.
Here we seed ~40 real-world and representative grants so the system works
fully offline and can be extended without touching the API layer.
"""
from __future__ import annotations
from typing import List
from backend.models import GrantOpportunity

# ---------------------------------------------------------------------------
# Seed data — representative global startup grants & funding programmes
# ---------------------------------------------------------------------------
SEED_GRANTS: List[dict] = [
    # ---- India ---------------------------------------------------------------
    {
        "id": "startup-india-seed",
        "title": "Startup India Seed Fund Scheme (SISFS)",
        "source": "DPIIT / Startup India",
        "url": "https://www.startupindia.gov.in/content/sih/en/funding.html",
        "description": (
            "Provides financial assistance to startups for proof of concept, "
            "prototype development, product trials, market entry, and "
            "commercialisation. Administered through DPIIT-recognised incubators."
        ),
        "eligibility": (
            "DPIIT-recognised startup, incorporated ≤ 2 years, not received "
            "prior funding > ₹50 lakh from GoI, must work through an empanelled incubator."
        ),
        "funding_amount": "Up to ₹20 lakh (PoC) / ₹50 lakh (commercialisation)",
        "deadline": "Rolling — quarterly incubator applications",
        "domain_tags": ["all", "deeptech", "agritech", "healthtech", "edtech", "cleanenergy"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["India"],
    },
    {
        "id": "birac-bionest",
        "title": "BIRAC BioNEST — Biotech Incubation Scheme",
        "source": "BIRAC (Govt. of India)",
        "url": "https://birac.nic.in/bionest.php",
        "description": (
            "Supports biotech, medtech, and agri-biotech startups through "
            "incubation infrastructure, mentorship, and seed funding."
        ),
        "eligibility": (
            "Early-stage biotech / medtech / agri-biotech startup, Indian entity, "
            "incorporated ≤ 5 years."
        ),
        "funding_amount": "Up to ₹50 lakh seed grant",
        "deadline": "Open calls — check BIRAC website",
        "domain_tags": ["healthtech", "biotech", "agritech", "medtech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["India"],
    },
    {
        "id": "tide-meity",
        "title": "TIDE 2.0 — Technology Incubation and Development of Entrepreneurs",
        "source": "MeitY (Govt. of India)",
        "url": "https://tide.meity.gov.in/",
        "description": (
            "Supports ICT-based startups through incubators. Provides seed funding, "
            "mentorship, and tech infrastructure for AI/ML, IoT, blockchain, and cybersecurity startups."
        ),
        "eligibility": (
            "ICT / software / AI startups, Indian entity, working through a TIDE-empanelled incubator."
        ),
        "funding_amount": "Up to ₹75 lakh",
        "deadline": "Rolling — through empanelled incubators",
        "domain_tags": ["ai/ml", "iot", "blockchain", "cybersecurity", "fintech", "edtech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["India"],
    },
    {
        "id": "nidhi-prayas",
        "title": "NIDHI PRAYAS — Proof of Concept Grant",
        "source": "DST / NSTEDB (Govt. of India)",
        "url": "https://nidhi.dst.gov.in/prayas",
        "description": (
            "Supports individual innovators and early-stage startups to build "
            "a working prototype from an idea or concept stage."
        ),
        "eligibility": (
            "Indian individual innovator or early-stage startup, working through "
            "a NIDHI-PRAYAS empanelled host institution."
        ),
        "funding_amount": "Up to ₹10 lakh",
        "deadline": "Rolling",
        "domain_tags": ["all", "deeptech", "hardware", "medtech"],
        "stage_tags": ["Idea", "Pre-Seed"],
        "location_tags": ["India"],
    },
    {
        "id": "atal-avia",
        "title": "Atal Innovation Mission — Atal Incubation Centres (AIC)",
        "source": "NITI Aayog / AIM",
        "url": "https://aim.gov.in/atal-incubation-centres.php",
        "description": (
            "Establishes world-class incubation centres to foster innovative "
            "startups across sectors. Provides grant support to incubators that "
            "then fund and mentor startups."
        ),
        "eligibility": (
            "Indian startup, any sector, incubated at or applying through an AIC. "
            "Preference for Tier-2/3 city startups."
        ),
        "funding_amount": "Up to ₹10 crore to the incubator; startups get equity-free support",
        "deadline": "Periodic — check AIM website",
        "domain_tags": ["all", "agritech", "healthtech", "cleanenergy", "edtech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["India"],
    },
    # ---- USA -----------------------------------------------------------------
    {
        "id": "sbir-sttr",
        "title": "SBIR / STTR — Small Business Innovation Research",
        "source": "US Federal Government",
        "url": "https://www.sbir.gov/",
        "description": (
            "America's largest source of early-stage R&D funding for small businesses. "
            "Phase I validates concept; Phase II expands R&D; Phase III commercialises."
        ),
        "eligibility": (
            "US-based for-profit small business (<500 employees), majority US-owned, "
            "principal investigator employed by the company."
        ),
        "funding_amount": "Phase I: up to $275K; Phase II: up to $1.83M",
        "deadline": "Varies by agency — rolling solicitations",
        "domain_tags": ["all", "deeptech", "healthtech", "cleanenergy", "ai/ml", "cybersecurity"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["USA"],
    },
    {
        "id": "nsf-innovation-corps",
        "title": "NSF I-Corps — Innovation Corps",
        "source": "National Science Foundation (USA)",
        "url": "https://www.nsf.gov/news/special_reports/i-corps/",
        "description": (
            "Trains NSF-funded researchers and early-stage startups to evaluate "
            "commercial potential of their innovations through customer discovery."
        ),
        "eligibility": (
            "Startup or researcher with NSF-funded research background, "
            "US-based team."
        ),
        "funding_amount": "Up to $50,000 (National Teams)",
        "deadline": "Cohort-based — check NSF I-Corps website",
        "domain_tags": ["all", "deeptech", "ai/ml", "cleanenergy", "healthtech"],
        "stage_tags": ["Idea", "Pre-Seed"],
        "location_tags": ["USA"],
    },
    {
        "id": "doe-office-energy",
        "title": "DOE Office of Energy Efficiency — Clean Energy Incubator Fund",
        "source": "US Dept. of Energy",
        "url": "https://www.energy.gov/eere/funding",
        "description": (
            "Funds clean energy technology development from early R&D through "
            "commercialisation. Supports solar, wind, storage, hydrogen, and efficiency."
        ),
        "eligibility": (
            "US-based startup or SME in clean energy, must meet solicitation-specific requirements."
        ),
        "funding_amount": "$500K – $5M per award",
        "deadline": "Solicitation-specific — check EERE Exchange",
        "domain_tags": ["cleanenergy", "hardware", "deeptech"],
        "stage_tags": ["Seed", "Series-A"],
        "location_tags": ["USA"],
    },
    # ---- EU ------------------------------------------------------------------
    {
        "id": "eic-accelerator",
        "title": "EIC Accelerator — European Innovation Council",
        "source": "European Commission",
        "url": "https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en",
        "description": (
            "Flagship EU programme supporting high-impact, market-creating startups "
            "and SMEs. Blended finance: grant component + equity investment."
        ),
        "eligibility": (
            "SME or startup from EU member state or associated country, "
            "breakthrough or deep-tech innovation, ready for scale-up."
        ),
        "funding_amount": "Grant up to €2.5M + equity up to €15M",
        "deadline": "Three cut-off dates per year",
        "domain_tags": ["deeptech", "healthtech", "cleanenergy", "ai/ml", "biotech"],
        "stage_tags": ["Seed", "Series-A", "Growth"],
        "location_tags": ["Europe", "EU"],
    },
    {
        "id": "horizon-europe-msca",
        "title": "Horizon Europe — Marie Skłodowska-Curie Actions (MSCA)",
        "source": "European Commission",
        "url": "https://marie-sklodowska-curie-actions.ec.europa.eu/",
        "description": (
            "Funds researcher mobility and knowledge exchange. Startups can "
            "host researchers or co-develop projects under the MSCA-SE scheme."
        ),
        "eligibility": (
            "EU or associated country entity, any sector, research-based project."
        ),
        "funding_amount": "€150K – €2.7M depending on scheme",
        "deadline": "Annual calls",
        "domain_tags": ["all", "deeptech", "ai/ml", "healthtech"],
        "stage_tags": ["Pre-Seed", "Seed", "Series-A"],
        "location_tags": ["Europe", "EU"],
    },
    # ---- Global / Multilateral -----------------------------------------------
    {
        "id": "world-bank-infdev",
        "title": "World Bank infoDev — Startup Catalyst",
        "source": "World Bank Group",
        "url": "https://www.infodev.org/",
        "description": (
            "Supports entrepreneurs and innovation ecosystems in developing countries "
            "through grants, incubators, and accelerators."
        ),
        "eligibility": (
            "Startup from a developing / emerging economy, social or economic impact focus."
        ),
        "funding_amount": "$50K – $500K",
        "deadline": "Programme-specific",
        "domain_tags": ["agritech", "fintech", "healthtech", "edtech", "cleanenergy"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["Global", "Africa", "South Asia", "Latin America"],
    },
    {
        "id": "unep-climate-innovation",
        "title": "UNEP Climate Innovation Centres",
        "source": "United Nations Environment Programme",
        "url": "https://www.unep.org/",
        "description": (
            "Accelerates clean-tech and climate startups in developing nations "
            "through business development, funding access, and mentorship."
        ),
        "eligibility": (
            "Climate-focused startup, based in a developing country eligible for UNEP support."
        ),
        "funding_amount": "Up to $100K equity-free grant",
        "deadline": "Rolling — country-specific calls",
        "domain_tags": ["cleanenergy", "agritech", "deeptech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["Global", "Africa", "South Asia"],
    },
    {
        "id": "ibm-hyper-protect",
        "title": "IBM Hyper Protect Accelerator — HealthTech & FinTech",
        "source": "IBM",
        "url": "https://www.ibm.com/partnerplus/isv/ibm-hyper-protect-accelerator",
        "description": (
            "IBM's flagship accelerator for HealthTech and FinTech startups. "
            "Provides IBM Cloud credits, Granite AI access, mentorship from IBM executives, "
            "and investor introductions."
        ),
        "eligibility": (
            "HealthTech or FinTech startup, Series A or earlier, "
            "product must have a data security or compliance use-case."
        ),
        "funding_amount": "$120,000 in IBM Cloud credits + investor access",
        "deadline": "Annual cohort — check IBM partner portal",
        "domain_tags": ["healthtech", "fintech", "ai/ml", "cybersecurity"],
        "stage_tags": ["Pre-Seed", "Seed", "Series-A"],
        "location_tags": ["Global"],
    },
    {
        "id": "google-black-founders",
        "title": "Google for Startups — Black Founders Fund",
        "source": "Google",
        "url": "https://startup.google.com/programs/black-founders-fund/",
        "description": (
            "Non-dilutive cash awards and Google Cloud credits to Black-led startups "
            "across the US, UK, Europe, and Africa."
        ),
        "eligibility": (
            "Black-led startup, Seed–Series A, US, UK, European or African entity."
        ),
        "funding_amount": "$100K cash + $200K Google Cloud credits (US); varies by region",
        "deadline": "Annual — check Google for Startups website",
        "domain_tags": ["all", "ai/ml", "edtech", "fintech", "healthtech"],
        "stage_tags": ["Pre-Seed", "Seed", "Series-A"],
        "location_tags": ["USA", "UK", "Europe", "Africa", "Global"],
    },
    {
        "id": "microsoft-for-startups",
        "title": "Microsoft for Startups Founders Hub",
        "source": "Microsoft",
        "url": "https://foundershub.startups.microsoft.com/",
        "description": (
            "Provides Azure credits, GitHub, Microsoft 365, and Azure OpenAI access "
            "to help startups build and scale their products."
        ),
        "eligibility": (
            "Any startup (idea stage to Series A), no revenue requirement. "
            "Apply online — fast approval."
        ),
        "funding_amount": "Up to $150,000 Azure credits",
        "deadline": "Rolling — always open",
        "domain_tags": ["all", "ai/ml", "saas", "fintech", "edtech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed", "Series-A"],
        "location_tags": ["Global"],
    },
    {
        "id": "aws-activate",
        "title": "AWS Activate — Startup Credits",
        "source": "Amazon Web Services",
        "url": "https://aws.amazon.com/activate/",
        "description": (
            "Provides AWS credits, training, and support to early-stage startups "
            "to help them build on AWS infrastructure."
        ),
        "eligibility": (
            "Early-stage startup (<5 years old), not yet AWS customer or limited prior credits. "
            "Portfolio tier requires an accelerator/incubator affiliation."
        ),
        "funding_amount": "Up to $100,000 AWS credits",
        "deadline": "Rolling",
        "domain_tags": ["all", "ai/ml", "saas", "deeptech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["Global"],
    },
    # ---- AgriTech specialised ------------------------------------------------
    {
        "id": "agri-udaan",
        "title": "AgriUdaan — Agri-Food Tech Accelerator",
        "source": "NAARM / ICAR (India)",
        "url": "https://www.naarm.org.in/",
        "description": (
            "Accelerates agri-food tech startups in India with mentorship from "
            "ICAR scientists, government network access, and seed funding."
        ),
        "eligibility": (
            "Indian startup in agri-food, FoodTech, or rural tech sector, "
            "revenue < ₹1 crore."
        ),
        "funding_amount": "₹5–15 lakh equity-free grant + in-kind support",
        "deadline": "Annual cohort — check NAARM website",
        "domain_tags": ["agritech", "foodtech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["India"],
    },
    # ---- CleanTech / CleanEnergy specialised ---------------------------------
    {
        "id": "climatelaunchpad",
        "title": "ClimateLaunchpad — Green Business Competition",
        "source": "European Institute of Innovation & Technology (EIT Climate-KIC)",
        "url": "https://climatelaunchpad.org/",
        "description": (
            "World's largest green business ideas competition. Supports clean-tech "
            "entrepreneurs from idea to investment-ready stage."
        ),
        "eligibility": (
            "Clean-tech startup or idea team, 70+ countries eligible, "
            "pre-revenue or early revenue."
        ),
        "funding_amount": "€10,000–€50,000 + acceleration programme",
        "deadline": "Annual — national heats followed by global finale",
        "domain_tags": ["cleanenergy", "agritech", "deeptech"],
        "stage_tags": ["Idea", "Pre-Seed"],
        "location_tags": ["Global", "Europe"],
    },
    # ---- HealthTech / MedTech ------------------------------------------------
    {
        "id": "wellcome-innovator",
        "title": "Wellcome Innovator Awards",
        "source": "Wellcome Trust (UK)",
        "url": "https://wellcome.org/grant-funding/schemes/innovator-awards",
        "description": (
            "Supports early-stage health innovation — including diagnostics, "
            "therapeutics, digital health, and medical devices."
        ),
        "eligibility": (
            "UK or LMIC-based researcher or startup, health-focused innovation, "
            "project must be at proof-of-concept stage."
        ),
        "funding_amount": "£50K–£500K over 18–24 months",
        "deadline": "Quarterly expression of interest rounds",
        "domain_tags": ["healthtech", "medtech", "biotech"],
        "stage_tags": ["Idea", "Pre-Seed", "Seed"],
        "location_tags": ["UK", "Global"],
    },
    # ---- EdTech --------------------------------------------------------------
    {
        "id": "gates-edtech",
        "title": "Bill & Melinda Gates Foundation — Education Innovation Grant",
        "source": "Bill & Melinda Gates Foundation",
        "url": "https://www.gatesfoundation.org/our-work/programs/us-program/postsecondary-success",
        "description": (
            "Funds EdTech innovations that improve educational equity, student "
            "completion rates, and workforce readiness."
        ),
        "eligibility": (
            "Non-profit or for-profit EdTech startup, focus on underserved student populations, "
            "US or global developing country."
        ),
        "funding_amount": "$100K – $2M",
        "deadline": "By invitation / limited RFP cycles",
        "domain_tags": ["edtech", "ai/ml"],
        "stage_tags": ["Seed", "Series-A"],
        "location_tags": ["USA", "Global"],
    },
    # ---- Fintech -------------------------------------------------------------
    {
        "id": "rbi-regulatory-sandbox",
        "title": "RBI Regulatory Sandbox — FinTech",
        "source": "Reserve Bank of India",
        "url": "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx",
        "description": (
            "Allows FinTech startups to live-test new financial products and services "
            "under a relaxed regulatory framework with RBI oversight."
        ),
        "eligibility": (
            "Indian FinTech company, net worth ≥ ₹25 lakh, fit and proper criteria. "
            "Cohort themes change per cycle."
        ),
        "funding_amount": "Regulatory access (non-financial grant)",
        "deadline": "Cohort-based — check RBI press releases",
        "domain_tags": ["fintech", "blockchain"],
        "stage_tags": ["Seed", "Series-A"],
        "location_tags": ["India"],
    },
    # ---- Deep Tech / AI ------------------------------------------------------
    {
        "id": "nasscom-deeptech",
        "title": "NASSCOM DeepTech Club — Startup Support",
        "source": "NASSCOM",
        "url": "https://nasscom.in/deep-tech",
        "description": (
            "Connects deep-tech startups (AI/ML, robotics, quantum, space-tech) "
            "with enterprise partners, investors, and policy support."
        ),
        "eligibility": "Indian AI/ML, robotics, quantum, or space-tech startup.",
        "funding_amount": "Non-monetary — enterprise connects, pilot opportunities",
        "deadline": "Rolling membership",
        "domain_tags": ["ai/ml", "deeptech", "robotics"],
        "stage_tags": ["Seed", "Series-A", "Growth"],
        "location_tags": ["India"],
    },
]


def get_all_grants() -> List[GrantOpportunity]:
    """Return all seed grants as GrantOpportunity objects."""
    grants: List[GrantOpportunity] = []
    for g in SEED_GRANTS:
        grants.append(
            GrantOpportunity(
                id=g["id"],
                title=g["title"],
                source=g["source"],
                url=g["url"],
                description=g["description"],
                eligibility=g["eligibility"],
                funding_amount=g["funding_amount"],
                deadline=g["deadline"],
                domain_tags=g.get("domain_tags", []),
                stage_tags=g.get("stage_tags", []),
                location_tags=g.get("location_tags", []),
            )
        )
    return grants
