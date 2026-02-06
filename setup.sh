#!/bin/bash

echo "================================================"
echo "  MindCare Mental Health App - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

echo ""
echo "Installing required packages..."
echo "This may take a few minutes..."
echo ""

# Install packages
pip install streamlit pandas plotly python-dateutil

echo ""
echo "================================================"
echo "  Installation Complete!"
echo "================================================"
echo ""
echo "To run the application, use:"
echo "  streamlit run app.py"
echo ""
echo "The app will open in your default browser."
echo "If not, navigate to: http://localhost:8501"
echo ""
echo "================================================"
