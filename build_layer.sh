#!/bin/bash

# Create directories
mkdir -p dependencies/python

# Install dependencies
pip install -r requirements.txt -t dependencies/python

# Remove unnecessary files
find dependencies/python -type d -name "__pycache__" -exec rm -rf {} +
find dependencies/python -type d -name "*.dist-info" -exec rm -rf {} +
find dependencies/python -type d -name "*.egg-info" -exec rm -rf {} +

# Create zip file
cd dependencies
zip -r ../dependencies.zip .
cd ..

# Clean up
rm -rf dependencies 