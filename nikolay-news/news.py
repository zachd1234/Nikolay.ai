#!/usr/bin/env python3
"""
AI News Weekly Generator using OpenRouter
This script generates weekly AI news summaries using OpenRouter's API.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AINewsGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI News Generator with OpenRouter API key."""
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key not found. Please set OPENROUTER_API_KEY in your .env file.\n"
                "You can copy .env.example to .env and add your API key."
            )
        
        self.base_url = "https://openrouter.ai/api/v1"
        # Load model from environment variable or use default
        self.model = os.getenv("OPENROUTER_MODEL", "z-ai/glm-4.6")
        
        # Check if model is explicitly set to empty
        if os.getenv("OPENROUTER_MODEL") == "":
            raise ValueError(
                "OpenRouter model is set to empty. Please set OPENROUTER_MODEL in your .env file.\n"
                "You can see available models with: python news.py --list-models"
            )
    
    def generate_news_prompt(self, days_back: int = 7) -> str:
        """Generate a prompt for AI news based on the specified number of days back."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        prompt = f"""
        Please generate a comprehensive weekly AI news summary covering the period from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.
        
        Include the following sections:
        1. Major AI Model Releases and Updates
        2. Industry News and Partnerships
        3. Research Breakthroughs
        4. Regulatory and Policy Updates
        5. Notable AI Applications and Use Cases
        
        For each section, provide:
        - Brief description of the news item
        - Key companies or researchers involved
        - Potential impact on the AI industry
        
        Format the output as a well-structured markdown document with appropriate headings, bullet points, and links where relevant.
        Make it informative yet concise, suitable for a weekly newsletter.
        """
        
        return prompt
    
    def call_openrouter(self, prompt: str) -> str:
        """Make a request to OpenRouter API."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except requests.exceptions.RequestException as e:
            print(f"Error making request to OpenRouter: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            sys.exit(1)
        except (KeyError, IndexError) as e:
            print(f"Error parsing response from OpenRouter: {e}")
            sys.exit(1)
    
    def generate_news(self, days_back: int = 7, output_file: Optional[str] = None) -> str:
        """Generate AI news for the specified period."""
        print(f"Generating AI news for the past {days_back} days...")
        
        prompt = self.generate_news_prompt(days_back)
        news_content = self.call_openrouter(prompt)
        
        # Add header with generation date
        header = f"""# AI News Weekly Report
        
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Covering the period from {(datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}*

---

"""
        
        full_content = header + news_content
        
        # Default to saving in news_database with timestamp if no output file specified
        if not output_file:
            # Create news_database directory if it doesn't exist
            os.makedirs("news_database", exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"news_database/ai_news_{timestamp}.md"
        
        if output_file:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_content)
            print(f"AI news saved to {output_file}")
        
        return full_content
    
    def list_available_models(self) -> List[Dict]:
        """List available models from OpenRouter."""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers
            )
            response.raise_for_status()
            
            models_data = response.json()
            return models_data.get("data", [])
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching models from OpenRouter: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(description="Generate AI news weekly using OpenRouter")
    parser.add_argument("--days", type=int, default=7, help="Number of days back to cover (default: 7)")
    parser.add_argument("--output", "-o", type=str, help="Output file path (default: print to console)")
    parser.add_argument("--model", "-m", type=str, help="OpenRouter model to use")
    parser.add_argument("--list-models", action="store_true", help="List available models and exit")
    
    args = parser.parse_args()
    
    try:
        generator = AINewsGenerator()
        
        if args.model:
            generator.model = args.model
        
        if args.list_models:
            models = generator.list_available_models()
            print("Available models:")
            for model in models:
                print(f"- {model['id']}: {model['name']}")
            return
        
        news_content = generator.generate_news(days_back=args.days, output_file=args.output)
        
        # Always display the content unless explicitly saved to a file
        if not args.output:
            print("\n--- Generated AI News ---")
            print(news_content)
    
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
