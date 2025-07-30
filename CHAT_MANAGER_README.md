# WhatsApp Chat Manager

A web-based interface to manage WhatsApp conversations with manual replies and AI automation.

## Features

- **Real-time Chat Dashboard**: View all incoming WhatsApp messages
- **Manual Replies**: Send messages manually to any contact
- **AI Toggle**: Enable/disable AI auto-replies per contact
- **Message History**: Track all conversations with timestamps
- **Source Tracking**: See which messages were sent manually vs AI

## Quick Start

1. **Start the Chat Manager**:
   ```bash
   python start_chat_manager.py
   ```

2. **Open Dashboard**: 
   - Go to `http://localhost:3000`
   - View all active chats in the left panel
   - Select a contact to view conversation

3. **Test the System**:
   ```bash
   python test_chat_manager.py
   ```

## Usage

### Manual Chat Management
1. Select a contact from the left panel
2. Type your message in the input field
3. Click "Send" or press Enter
4. Message will be sent via WhatsApp API

### AI Auto-Replies
1. Select a contact
2. Click "AI: Disabled" button to enable AI
3. Button will turn green showing "AI: Enabled"
4. All incoming messages will get automatic AI responses
5. Click again to disable AI for manual handling

### Dashboard Features
- **Green AI Badge**: Shows contacts with AI enabled
- **Message Badges**: 
  - Blue "AI" badge for AI-generated messages
  - Orange "Manual" badge for manually sent messages
- **Real-time Updates**: Dashboard refreshes every 3 seconds
- **Message History**: All messages stored with timestamps

## API Endpoints

- `GET /` - Dashboard interface
- `GET /api/chats` - Get all chats and AI status
- `POST /api/send` - Send manual message
- `POST /api/toggle-ai` - Toggle AI for contact
- `POST /webhook` - WhatsApp webhook endpoint

## Configuration

Uses the same `.env` file as the main WhatsApp bot:
- `WHATSAPP_TOKEN` - Tata Telecom API token
- `WHATSAPP_PHONE_NUMBER_ID` - Phone number ID
- `OPENAI_API_KEY` - OpenAI API key
- `VERIFY_TOKEN` - Webhook verification token

## Production Notes

- Currently uses in-memory storage (implement database for production)
- Add authentication for dashboard access
- Implement message persistence
- Add user management and permissions