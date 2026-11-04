"""
run.py — Start the Streamlit app.

Usage:
    python run.py
"""
import sys
import subprocess

subprocess.run(
    [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
    check=True,
)
