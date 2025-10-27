#!/bin/bash

# AI News Weekly Generator Runner Script

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found."
    echo ""
    echo "Please create a .env file with your OpenRouter API key and preferred model:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit the .env file with your actual values:"
    echo "  OPENROUTER_API_KEY=your_api_key_here"
    echo "  OPENROUTER_MODEL=anthropic/claude-3-haiku"
    echo ""
    echo "Get your API key from: https://openrouter.ai/keys"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the news generator with provided arguments
echo "Running AI News Weekly Generator..."
python news.py "$@"
