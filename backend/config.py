"""
config.py — Central configuration loaded from environment variables.
On Streamlit Cloud, secrets are read from st.secrets (set via the Secrets panel).
Locally, secrets are loaded from the .env file via python-dotenv.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def _get(key: str, default: str = "") -> str:
    """
    Read a config value: prefer st.secrets (Streamlit Cloud),
    then os.environ / .env file, then fall back to default.
    """
    try:
        import streamlit as st
        value = st.secrets.get(key)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(key, default)


IBM_API_KEY: str = _get("IBM_API_KEY", "")
IBM_PROJECT_ID: str = _get("IBM_PROJECT_ID", "")
IBM_WATSONX_URL: str = _get("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
GRANITE_MODEL_ID: str = _get("GRANITE_MODEL_ID", "ibm/granite-13b-instruct-v2")

APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
GRANT_CACHE_TTL: int = int(os.getenv("GRANT_CACHE_TTL", "3600"))
