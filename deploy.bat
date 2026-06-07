@echo off
title Textile ERP - High-Speed Netlify Auto-Deployer
echo ===================================================
echo   Textile ERP - High-Speed Netlify Auto-Deployer
echo ===================================================
echo.
echo Step 1: Compiling optimized web build...
call npm run build
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed. Please check your Node.js/NPM installation.
    pause
    exit /b %errorlevel%
)
echo.
echo [SUCCESS] Web build generated successfully inside the 'dist' folder!
echo.
echo Step 2: Uploading to Netlify...
echo.
call npx netlify deploy --prod --dir=dist
echo.
echo ===================================================
echo   Deployment Process Completed!
echo ===================================================
pause
