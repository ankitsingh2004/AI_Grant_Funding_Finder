"""
config.py — Central configuration loaded from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

IBM_API_KEY: str = os.getenv("IBM_API_KEY", "")
IBM_PROJECT_ID: str = os.getenv("IBM_PROJECT_ID", "")
IBM_WATSONX_URL: str = os.getenv(
    "IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com"
)
GRANITE_MODEL_ID: str = os.getenv(
    "GRANITE_MODEL_ID", "ibm/granite-13b-instruct-v2"
)

APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
GRANT_CACHE_TTL: int = int(os.getenv("GRANT_CACHE_TTL", "3600"))
