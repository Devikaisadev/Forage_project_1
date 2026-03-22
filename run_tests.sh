#!/bin/bash

# Step 1 — Activate the virtual environment
source venv/Scripts/activate

# Install required packages
pip install dash pandas plotly dash[testing] selenium webdriver-manager chromedriver-autoinstaller --quiet

# Step 2 — Execute the test suite
python -m pytest test_visualisation.py -v --headless

# Step 3 — Return exit code
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi