@echo off
echo.
echo ==========================================
echo   Darukaa.Earth AI Biodiversity Platform
echo   Starting Frontend (Vite/React)
echo ==========================================
echo.

cd /d "%~dp0\frontend"

:: Install npm packages if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

:: Start Vite dev server
echo.
echo Starting Vite dev server on http://localhost:5173
echo.
npm run dev
