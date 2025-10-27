#!/usr/bin/env python3
"""
Generate HTML invitation for hack event using the latest AI news
"""

import os
import re
import glob
from datetime import datetime, timedelta
from pathlib import Path

def get_latest_news_file():
    """Get the most recent news file from news_database directory."""
    news_files = glob.glob("news_database/ai_news_*.md")
    if not news_files:
        raise FileNotFoundError("No news files found in news_database directory")
    
    # Sort by modification time, get the latest
    latest_file = max(news_files, key=os.path.getmtime)
    return latest_file

def extract_news_content(file_path):
    """Extract and format news content from markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the header part
    content = re.sub(r'# AI News Weekly Report.*?---\n\n', '', content, flags=re.DOTALL)
    
    # Convert markdown headers to HTML
    content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    
    # Convert markdown lists to HTML
    content = re.sub(r'^- (.*?)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', content, flags=re.DOTALL)
    
    # Convert markdown bold to HTML
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    
    # Convert markdown links to HTML
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # Convert line breaks to HTML
    content = re.sub(r'\n\n', '</p><p>', content)
    content = f'<p>{content}</p>'
    
    # Fix nested lists
    content = re.sub(r'<p><ul>', '<ul>', content)
    content = re.sub(r'</ul></p>', '</ul>', content)
    
    return content

def generate_html_invitation(news_content):
    """Generate the HTML invitation with news content and assets."""
    # Calculate date for next week (7 days from now)
    next_week = datetime.now() + timedelta(days=7)
    event_date = next_week.strftime("%B %d, %Y")
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nikolay.ai Hack Event Invitation</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            text-align: center;
            margin-bottom: 30px;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .logo {{
            max-width: 200px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .event-details {{
            background-color: #e9f7fe;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .news-section {{
            background-color: #fff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .news-section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .news-section h3 {{
            color: #34495e;
            margin-top: 25px;
        }}
        .news-section ul {{
            margin-left: 20px;
        }}
        .news-section li {{
            margin-bottom: 10px;
        }}
        footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background-color: #2c3e50;
            color: #ecf0f1;
            border-radius: 10px;
        }}
        .video-container {{
            margin-top: 20px;
        }}
        video {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .cta-button {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
            transition: background-color 0.3s;
        }}
        .cta-button:hover {{
            background-color: #2980b9;
        }}
        .registration-section {{
            background-color: #fff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .registration-form {{
            max-width: 500px;
            margin: 0 auto;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .form-group input {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        .form-group input:focus {{
            border-color: #3498db;
            outline: none;
            box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
        }}
        .message {{
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            display: none;
        }}
        .success {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .error {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        .info {{
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <img src="assets/logo.png" alt="Nikolay.ai Logo" class="logo">
            <h1>You're Invited to Nikolay.ai Hack Event!</h1>
            <p>Join us for an exciting weekend of innovation and AI development</p>
            <div class="event-details">
                <h3>Event Details</h3>
                <p><strong>Date:</strong> {event_date}</p>
                <p><strong>Location:</strong> Virtual & In-Person Options Available</p>
                <p><strong>Theme:</strong> Building the Future with AI</p>
            </div>
            <a href="#register" class="cta-button">Register Now</a>
        </header>

        <main>
            <section class="news-section">
                <h2>Latest AI News & Insights</h2>
                <p>Stay updated with the latest developments in AI that will inspire your hackathon projects:</p>
                {news_content}
            </section>
            
            <section class="registration-section" id="register">
                <h2>Register for the Event</h2>
                <div class="registration-form">
                    <form id="registrationForm">
                        <div class="form-group">
                            <label for="email">Email Address *</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="name">Full Name</label>
                            <input type="text" id="name" name="name">
                        </div>
                        <div class="form-group">
                            <label for="organization">Organization</label>
                            <input type="text" id="organization" name="organization">
                        </div>
                        <button type="submit" class="cta-button">Register</button>
                    </form>
                    <div id="registrationMessage" class="message"></div>
                </div>
            </section>
        </main>

        <footer>
            <h2>About Nikolay.ai</h2>
            <p>Nikolay.ai is dedicated to fostering innovation in AI and bringing together the brightest minds to solve real-world challenges.</p>
            
            <div class="video-container">
                <video autoplay loop muted playsinline>
                    <source src="assets/nikolayTalk.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            
            <p id="register">Ready to join the hack event? Register today and be part of the AI revolution!</p>
            <a href="#" class="cta-button">Register for the Event</a>
        </footer>
    </div>

    <script>
        // Form submission handler
        document.addEventListener('DOMContentLoaded', function() {{
            // Get form and message elements
            const form = document.getElementById('registrationForm');
            const messageDiv = document.getElementById('registrationMessage');
            
            // Handle form submission
            form.addEventListener('submit', async function(e) {{
                e.preventDefault();
                
                // Get form data
                const formData = new FormData(form);
                const data = {{
                    email: formData.get('email'),
                    name: formData.get('name'),
                    organization: formData.get('organization')
                }};
                
                // Show loading message
                showMessage('Registering...', 'info');
                
                try {{
                    // Send registration request
                    const response = await fetch('/api/register', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify(data)
                    }});
                    
                    const result = await response.json();
                    
                    if (response.ok) {{
                        // Success
                        showMessage(result.message, 'success');
                        form.reset();
                    }} else {{
                        // Error
                        showMessage(result.detail || 'Registration failed', 'error');
                    }}
                }} catch (error) {{
                    // Network error
                    showMessage('Network error. Please try again.', 'error');
                    console.error('Registration error:', error);
                }}
            }});
            
            // Function to show messages
            function showMessage(message, type) {{
                messageDiv.textContent = message;
                messageDiv.className = 'message ' + type;
                messageDiv.style.display = 'block';
                
                // Auto-hide success messages after 5 seconds
                if (type === 'success') {{
                    setTimeout(() => {{
                        messageDiv.style.display = 'none';
                    }}, 5000);
                }}
            }}
            
            // Add smooth scrolling
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }});
            }});
            
            // Add animation to elements when they come into view
            const observerOptions = {{
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            }};
            
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = 1;
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, observerOptions);
            
            // Observe all sections
            document.querySelectorAll('section').forEach(section => {{
                section.style.opacity = 0;
                section.style.transform = 'translateY(20px)';
                section.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                observer.observe(section);
            }});
        }});
    </script>
</body>
</html>
"""
    
    return html_template

def main():
    """Main function to generate the HTML invitation."""
    try:
        # Get the latest news file
        latest_file = get_latest_news_file()
        print(f"Using latest news file: {latest_file}")
        
        # Extract news content
        news_content = extract_news_content(latest_file)
        
        # Generate HTML invitation
        html_content = generate_html_invitation(news_content)
        
        # Save the HTML file
        output_file = "hack_event_invitation.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML invitation generated: {output_file}")
        print("Open this file in your browser to view the invitation.")
        
    except Exception as e:
        print(f"Error generating HTML invitation: {e}")

if __name__ == "__main__":
    main()
