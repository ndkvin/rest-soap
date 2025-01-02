#!/bin/bash

# Create a virtual environment if no exist
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate the virtual environment
source .venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run the server using uvicorn
uvicorn server:fastapi_app --reload