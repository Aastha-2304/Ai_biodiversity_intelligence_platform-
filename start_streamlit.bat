@echo off
echo.
echo ==========================================
echo   Darukaa.Earth AI Biodiversity Platform
echo   Starting Streamlit App
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

:: Start the Streamlit app
echo.
echo Starting Streamlit app on http://localhost:8501
echo.
streamlit run app.py
