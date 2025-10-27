#!/usr/bin/env python3
"""
Runner script for Nikolay.ai Hack Event
This script generates AI news and creates an HTML invitation for the hack event.
"""

import os
import sys
import subprocess
from datetime import datetime

def run_news_generation():
    """Run the news.py script to generate the latest AI news."""
    print("Generating latest AI news...")
    try:
        # Run the news.py script
        result = subprocess.run([sys.executable, "news.py"], 
                              capture_output=True, text=True, check=True)
        print("✓ AI news generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating AI news: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ news.py script not found. Make sure it's in the same directory.")
        return False

def run_html_generation():
    """Run the generate_invitation.py script to create the HTML invitation."""
    print("Generating HTML invitation...")
    try:
        # Run the generate_invitation.py script
        result = subprocess.run([sys.executable, "generate_invitation.py"], 
                              capture_output=True, text=True, check=True)
        print("✓ HTML invitation generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error generating HTML invitation: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ generate_invitation.py script not found. Make sure it's in the same directory.")
        return False

def open_html_in_browser():
    """Open the generated HTML file in the default browser."""
    try:
        import webbrowser
        html_file = os.path.abspath("hack_event_invitation.html")
        if os.path.exists(html_file):
            print(f"Opening {html_file} in your default browser...")
            webbrowser.open(f"file://{html_file}")
            return True
        else:
            print("✗ HTML invitation file not found.")
            return False
    except Exception as e:
        print(f"✗ Error opening browser: {e}")
        return False

def main():
    """Main function to run the complete hack event preparation."""
    print("=" * 60)
    print("Nikolay.ai Hack Event Preparation")
    print("=" * 60)
    
    # Check if required files exist
    required_files = ["news.py", "generate_invitation.py", "assets/logo.png", "assets/nikolayTalk.mp4"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("✗ Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease make sure all required files are present before running this script.")
        sys.exit(1)
    
    # Step 1: Generate AI news
    if not run_news_generation():
        print("\n✗ Failed to generate AI news. Please check the error messages above.")
        sys.exit(1)
    
    print("\n" + "-" * 40)
    
    # Step 2: Generate HTML invitation
    if not run_html_generation():
        print("\n✗ Failed to generate HTML invitation. Please check the error messages above.")
        sys.exit(1)
    
    print("\n" + "-" * 40)
    
    # Step 3: Open HTML in browser
    if open_html_in_browser():
        print("✓ HTML invitation opened in browser")
    else:
        print("ℹ You can manually open hack_event_invitation.html in your browser")
    
    print("\n" + "=" * 60)
    print("Hack event preparation completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the generated HTML invitation")
    print("2. Customize the event details if needed")
    print("3. Share the HTML file with potential participants")
    print("4. Set up a registration system for the event")

if __name__ == "__main__":
    main()
