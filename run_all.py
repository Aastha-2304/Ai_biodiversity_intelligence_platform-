"""
Darukaa.Earth — Unified Single-Localhost Launcher
Starts both the Streamlit platform and FastAPI gateway, exposing all services
(React UI, Streamlit 6-Panel Intelligence, and FastAPI REST APIs) under ONE localhost:
 http://localhost:8000
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = ROOT_DIR / "frontend" / "dist"

def ensure_frontend_built():
    """Ensures React frontend distribution is compiled."""
    if not (FRONTEND_DIST / "index.html").exists():
        print(" Building React frontend distribution (first-time setup)...")
        subprocess.run(["npm", "run", "build"], cwd=str(ROOT_DIR / "frontend"), check=True, shell=True)
        print(" React build completed.")
    else:
        print(" React frontend distribution found at frontend/dist.")

def main():
    ensure_frontend_built()

    print("\n" + "=" * 72)
    print(" DARUKAA.EARTH — UNIFIED SINGLE-LOCALHOST PLATFORM")
    print("=" * 72)
    print(" Starting internal Streamlit engine on port 8501...")
    
    log_dir = ROOT_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    streamlit_log = open(log_dir / "streamlit.log", "w", encoding="utf-8")

    # 1. Start Streamlit in headless mode
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    streamlit_proc = subprocess.Popen(
        streamlit_cmd,
        cwd=str(ROOT_DIR),
        stdout=streamlit_log,
        stderr=streamlit_log
    )

    time.sleep(3)

    print(" Starting FastAPI Master Gateway on http://localhost:8000...")
    print("=" * 72)
    print(" UNIFIED LOCALHOST ACCESS:")
    print("   • Master Dashboard (React):      http://localhost:8000/")
    print("   • Streamlit Intelligence Portal: http://localhost:8000/streamlit")
    print("   • Interactive API Docs (Swagger):http://localhost:8000/docs")
    print("   • Backend API Health:            http://localhost:8000/api/health")
    print("=" * 72 + "\n")

    # 2. Start Uvicorn for FastAPI
    uvicorn_cmd = [
        sys.executable, "-m", "uvicorn", "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    try:
        uvicorn_proc = subprocess.Popen(uvicorn_cmd, cwd=str(ROOT_DIR))
        uvicorn_proc.wait()
    except KeyboardInterrupt:
        print("\n Shutting down unified platform...")
    finally:
        try:
            streamlit_proc.terminate()
            streamlit_proc.wait(timeout=2)
        except Exception:
            streamlit_proc.kill()
        print(" All processes terminated cleanly.")

if __name__ == "__main__":
    main()
