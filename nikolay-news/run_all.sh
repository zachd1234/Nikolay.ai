#!/bin/bash

# Nikolay.ai Complete Workflow Runner Script

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

# Check if required assets exist
if [ ! -f "assets/logo.png" ] || [ ! -f "assets/nikolayTalk.mp4" ]; then
    echo "Error: Required assets not found in assets/ directory."
    echo "Please ensure both logo.png and nikolayTalk.mp4 are present in the assets folder."
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

echo ""
echo "========================================"
echo "Nikolay.ai Complete Workflow"
echo "========================================"
echo ""

# Step 1: Generate AI news
echo "Step 1: Generating AI news..."
python news.py "$@"
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate AI news."
    exit 1
fi
echo "✓ AI news generated successfully"
echo ""

# Step 2: Generate HTML invitation
echo "Step 2: Generating HTML invitation..."
python generate_invitation.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate HTML invitation."
    exit 1
fi
echo "✓ HTML invitation generated successfully"
echo ""

# Step 3: Open HTML in browser (optional)
read -p "Do you want to open the HTML invitation in your browser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Opening HTML invitation in browser..."
    if command -v xdg-open > /dev/null; then
        xdg-open hack_event_invitation.html
    elif command -v open > /dev/null; then
        open hack_event_invitation.html
    else
        echo "Could not detect the web browser to use."
        echo "Please open hack_event_invitation.html manually in your browser."
    fi
fi

echo ""
echo "========================================"
echo "Complete workflow finished successfully!"
echo "========================================"
echo ""
echo "Generated files:"
echo "- AI news: news_database/ai_news_$(date +%Y%m%d)_*.md"
echo "- HTML invitation: hack_event_invitation.html"
echo ""
echo "Next steps:"
echo "1. Review the generated HTML invitation"
echo "2. Customize the event details if needed"
echo "3. Share the HTML file with potential participants"
