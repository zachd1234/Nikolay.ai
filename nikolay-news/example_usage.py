#!/usr/bin/env python3
"""
Example usage of the AINewsGenerator class
"""

from news import AINewsGenerator

def main():
    # Initialize the generator (it will automatically load the API key from .env)
    try:
        generator = AINewsGenerator()
        
        # Example 1: Generate news for the past 7 days (will save to news_database with timestamp)
        print("Example 1: Generating weekly AI news...")
        generator.generate_news(days_back=7)
        
        # Example 2: Generate news for the past 30 days and save to a specific file
        print("\nExample 2: Generating monthly AI news...")
        generator.generate_news(days_back=30, output_file="monthly_ai_news.md")
        
        # Example 3: Use a different model
        print("\nExample 3: Generating news with a different model...")
        generator.model = "openai/gpt-3.5-turbo"  # Override the model from .env
        generator.generate_news(days_back=7, output_file="ai_news_gpt3.md")
        
        print("\nAll examples completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
