# AI News Weekly Generator

This Python script uses OpenRouter's API to generate comprehensive weekly AI news summaries.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your OpenRouter API key and preferred model:
```
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=anthropic/claude-3-haiku
```

You can copy the provided `.env.example` file as a template:
```bash
cp .env.example .env
```

Then edit the `.env` file with your actual API key and preferred model.

To see available models, run:
```bash
python news.py --list-models
```

To get an API key:
- Visit [OpenRouter](https://openrouter.ai/keys)
- Sign up or log in to your account
- Generate a new API key

## Usage

### Basic Usage

Generate AI news for the past 7 days (default):
```bash
python news.py
```
The script will save the output to `news_database/ai_news_YYYYMMDD_HHMMSS.md` and display it in the console.

### Advanced Usage

Generate news for a custom number of days:
```bash
python news.py --days 14
```

Save the news to a specific file:
```bash
python news.py --output ai_news_weekly.md
```

Use a specific model:
```bash
python news.py --model openai/gpt-4
```

List available models:
```bash
python news.py --list-models
```

### Command Line Options

- `--days`: Number of days back to cover (default: 7)
- `--output, -o`: Output file path (default: print to console)
- `--model, -m`: OpenRouter model to use
- `--list-models`: List available models and exit

## Example Output

The script generates a well-structured markdown document with sections covering:
1. Major AI Model Releases and Updates
2. Industry News and Partnerships
3. Research Breakthroughs
4. Regulatory and Policy Updates
5. Notable AI Applications and Use Cases

## Automation

You can set up a cron job to run this script weekly:

```bash
# Edit crontab
crontab -e

# Add this line to run every Monday at 9 AM
0 9 * * 1 cd /path/to/your/project && python news.py --output weekly_ai_news_$(date +\%Y\%m\%d).md
```

## Hack Event Invitation

This project also includes tools to generate HTML invitations for hack events with registration functionality:

### Generate HTML Invitation

Create an HTML invitation for a hack event using the latest AI news:

```bash
python generate_invitation.py
```

This will:
1. Find the latest news file in news_database/
2. Extract and format the news content
3. Generate an HTML invitation with:
   - Logo at the top
   - Latest AI news content
   - Event details and registration information
   - Interactive registration form
   - Video playing in a loop at the bottom
   - Responsive design with smooth animations
4. Save it as hack_event_invitation.html

### Complete Hack Event Preparation

Run the complete workflow to generate news and create an HTML invitation:

**Option 1: Using Python script**
```bash
python run_hack_event.py
```

**Option 2: Using shell script (recommended)**
```bash
./run_all.sh
```

Both scripts will:
1. Generate the latest AI news using news.py
2. Create an HTML invitation using generate_invitation.py
3. The shell script will also offer to open the HTML in your browser

The shell script includes additional checks for required assets and provides a more interactive experience.

### Registration System

The HTML invitation includes an interactive registration form that:
- Collects user email address (required)
- Collects optional name and organization
- Validates email format
- Saves registrations to a MySQL database
- Provides real-time feedback to users

### Backend API

The registration system is powered by a FastAPI backend (`app.py`) that:
- Serves the HTML invitation
- Handles registration submissions
- Manages database connections
- Provides RESTful API endpoints

### Database Setup

The system uses MySQL to store registrations. The database table includes:
- Email (unique identifier)
- Name (optional)
- Organization (optional)
- Registration timestamp

### AWS Deployment

To deploy the application to AWS:

1. Prepare deployment files:
```bash
./deploy.sh
```

2. For local testing with Docker:
```bash
cd deploy_YYYYMMDD_HHMMSS
docker-compose up
```

3. For AWS deployment:
```bash
cd deploy_YYYYMMDD_HHMMSS
./deploy_aws.sh
```

The deployment script creates:
- Dockerfile for containerization
- docker-compose.yml for local testing
- AWS ECS task definition template
- Deployment script for AWS

### Environment Configuration

Create a `.env` file with your configuration:

```bash
# OpenRouter API Key
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=anthropic/claude-3-haiku

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=nikolay_hack_event
```

You can copy the provided `.env.example` file as a template:
```bash
cp .env.example .env
```

Then edit the `.env` file with your actual values.

## Troubleshooting

1. **API Key Error**: 
   - Make sure your `.env` file is properly configured with a valid OpenRouter API key.
   - The script will provide specific instructions if the API key is missing.

2. **Model Error**:
   - If the model is set to empty in your `.env` file, the script will alert you.
   - Use `--list-models` to see available models and choose one that exists.

3. **Request Failed**: 
   - Check your internet connection and OpenRouter service status.

4. **Missing .env File**:
   - The script will guide you to create a `.env` file from the provided template.
   - Run `cp .env.example .env` and then edit the file with your credentials.

## License

This project is open source and available under the MIT License.

