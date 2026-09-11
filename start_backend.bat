@echo off
echo.
echo ==========================================
echo   Darukaa.Earth AI Biodiversity Platform
echo   Starting Backend (FastAPI)
echo ==========================================
echo.

cd /d "%~dp0"

:: Check if venv exists
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

:: Activate venv
call .venv\Scripts\activate.bat

:: Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt --quiet

:: Start the FastAPI backend
echo.
echo Starting FastAPI server on http://localhost:8000
echo API Docs available at http://localhost:8000/docs
echo.
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
