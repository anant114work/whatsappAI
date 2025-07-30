# WhatsApp OpenAI Bot

A WhatsApp automation system that integrates with OpenAI to provide intelligent responses to messages.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment variables:**
   - Copy `.env` file and fill in your API credentials:
     - `WHATSAPP_TOKEN`: Your WhatsApp Business API access token
     - `WHATSAPP_PHONE_NUMBER_ID`: Your WhatsApp phone number ID
     - `VERIFY_TOKEN`: A custom token for webhook verification
     - `OPENAI_API_KEY`: Your OpenAI API key

3. **Get WhatsApp Business API Access:**
   - Create a Meta Business account
   - Set up WhatsApp Business API
   - Get your access token and phone number ID

4. **Get OpenAI API Key:**
   - Sign up at https://platform.openai.com/
   - Generate an API key

5. **Run the server:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

## Webhook Setup

1. Deploy your server to a public URL (use ngrok for testing)
2. Configure webhook URL in Meta Business Manager:
   - Webhook URL: `https://your-domain.com/webhook`
   - Verify token: Use the same token from your `.env` file

## Features

- Receives WhatsApp messages via webhook
- Processes messages with OpenAI GPT-3.5-turbo
- Sends intelligent responses back to users
- Error handling and logging

## Usage

Once configured, users can send messages to your WhatsApp Business number and receive AI-powered responses automatically.