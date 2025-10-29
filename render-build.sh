#!/usr/bin/env bash
# Alternative Render build script with better error handling

set -o errexit  # Exit on error

echo "=== Starting Build Process ==="

echo "Step 1: Upgrading pip..."
python -m pip install --upgrade pip

echo "Step 2: Installing Python dependencies..."
pip install -r requirements-light.txt

echo "Step 3: Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True)" || echo "NLTK download warning (non-critical)"

echo "Step 4: Verifying installations..."
python -c "import flask; print('Flask OK')"
python -c "import nltk; print('NLTK OK')"
python -c "import cv2; print('OpenCV OK')"

echo "=== Build Completed Successfully! ==="
