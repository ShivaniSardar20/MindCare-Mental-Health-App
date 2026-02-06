@echo off
echo ================================================
echo   MindCare Mental Health App - Setup Script
echo ================================================
echo.

echo Checking Python version...
python --version

echo.
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install streamlit pandas plotly python-dateutil

echo.
echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo To run the application, use:
echo   streamlit run app.py
echo.
echo The app will open in your default browser.
echo If not, navigate to: http://localhost:8501
echo.
echo ================================================
pause
