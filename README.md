# Nikolay.ai - Sundai Hacks Automation

## Overview
Nikolay.ai is an autonomous agent system designed to automatically set up and operate Sundai Hacks events.

## Project Goal
Get people to sign up for a hackathon next Friday by automating event creation, recruitment, and operations.

## System Architecture

### Setup Phase
The agent automatically sets up events by:
- **Email Marketing**: Sending promotional emails to Sundai's mailing list
- **Sponsor Outreach**: Email-pitching potential sponsors via Apollo.io
- **Venue Coordination**: Coordinating event location logistics

### Operations Phase
The agent operates events by:
- **Attendee Communication**: Conversational AI for attendee engagement
- **Food Ordering**: Automated catering for the event
- **Human-as-a-Tool**: Calling human assistance when needed for complex tasks

## Tools & Integrations

### Core Tools
- **Luma**: Event creation and management
- **Email**: Mailing list communication and sponsor outreach
- **Apollo.io**: Finding potential sponsors and attendees (trial)
- **Reddit**: Community engagement and promotion
- **Human-as-a-Tool**: Escalation for tasks requiring human intervention

## Actions Performed

### Setup Actions
1. Creates Luma event page
2. Recruits hackathon attendees
3. Recruits sponsors
4. Processes location requests

### Demo Focus
Initial demo will focus on the operating part of the system.

## Contact
- Email: Chaitvitaly@gmail.com

## Development Status
Currently in setup phase - building foundational automation infrastructure.

---

## Email CLI Tool

### Setup
1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure `.env` file with Gmail credentials (already configured):
   ```
   GMAIL_USER=ruckquest@gmail.com
   GMAIL_APP_PASSWORD=<your-app-password>
   ```

### Usage

Send an email via command line:

```bash
npm run send-email -- --to recipient@example.com --subject "Your Subject" --body "<h1>Hello</h1><p>This is HTML content</p>"
```

#### Options:
- `--to <email>` (required): Recipient email address
- `--subject <subject>` (required): Email subject line
- `--body <html>` (required): Email body (supports HTML/rich text format)
- `--cc <email>` (optional): CC email address

#### Examples:

**Simple text email:**
```bash
npm run send-email -- --to john@example.com --subject "Test Email" --body "<p>Hello World!</p>"
```

**Rich HTML email with CC:**
```bash
npm run send-email -- \
  --to attendee@example.com \
  --cc sponsor@example.com \
  --subject "Sundai Hacks - Next Friday" \
  --body "<h1>Join us at Sundai Hacks!</h1><p>Date: Next Friday</p><p>RSVP now!</p>"
```

**Multi-line HTML:**
```bash
npm run send-email -- \
  --to user@example.com \
  --subject "Event Announcement" \
  --body "<html><body><h1>Exciting News!</h1><p>We're hosting a hackathon.</p><ul><li>Free food</li><li>Great prizes</li><li>Networking</li></ul></body></html>"
```

### Build

Compile TypeScript to JavaScript:
```bash
npm run build
```

Compiled files will be in the `dist/` directory.
