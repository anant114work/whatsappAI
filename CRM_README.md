# 🚀 WhatsApp CRM System - Tata Integration

A comprehensive Customer Relationship Management system that integrates with Tata Telecom's WhatsApp Business API to provide a unified interface for managing all your WhatsApp conversations.

## ✨ Features

### 📱 Complete Conversation Management
- **All Historical Chats**: View all previous conversations from your Tata WhatsApp panel
- **Real-time Sync**: New messages appear instantly in the CRM
- **Message History**: Complete conversation history with timestamps
- **Contact Management**: Automatic contact creation and management

### 🤖 AI-Powered Responses
- **Automatic Replies**: AI generates intelligent responses to incoming messages
- **OpenAI Integration**: Uses GPT-4o-mini for natural conversations
- **Context Awareness**: AI understands conversation context

### 💬 Modern CRM Interface
- **WhatsApp-like UI**: Familiar chat interface
- **Contact Search**: Quick search through all contacts
- **Unread Messages**: Visual indicators for unread messages
- **Message Status**: Delivery status tracking
- **Responsive Design**: Works on desktop and mobile

### 🔗 Tata API Integration
- **Direct Integration**: Connects directly to Tata WhatsApp Business API
- **Webhook Support**: Receives real-time message notifications
- **Message Sending**: Send messages directly from CRM to WhatsApp
- **Template Support**: Support for WhatsApp message templates

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7+
- Tata WhatsApp Business API access
- OpenAI API key

### Quick Setup

1. **Clone and Navigate**
   ```bash
   cd whatsapp
   ```

2. **Configure Environment**
   Create/update `.env` file:
   ```env
   WHATSAPP_TOKEN=your_tata_whatsapp_token
   OPENAI_API_KEY=your_openai_api_key
   VERIFY_TOKEN=your_webhook_verify_token
   ```

3. **Run Setup**
   ```bash
   python setup_crm.py
   ```

4. **Start CRM**
   ```bash
   python start_crm.py
   ```

5. **Access CRM**
   Open: http://localhost:3000

### Webhook Configuration

Your webhook URL is: `https://whatsappai-x52i.onrender.com/webhook`

Configure this in your Tata WhatsApp Business panel to receive real-time messages.

## 📊 Database Schema

The CRM uses SQLite with three main tables:

### Contacts Table
- `phone`: Contact phone number (unique)
- `name`: Contact name
- `first_seen`: When contact first messaged
- `last_seen`: Last activity timestamp
- `total_messages`: Total message count
- `status`: Contact status (active/inactive)

### Messages Table
- `contact_phone`: Associated contact
- `message_text`: Message content
- `direction`: sent/received
- `timestamp`: Message timestamp
- `status`: Message delivery status
- `message_type`: text/image/document

### Conversations Table
- `contact_phone`: Associated contact
- `last_message`: Most recent message
- `last_message_time`: Timestamp of last message
- `unread_count`: Number of unread messages

## 🔧 API Endpoints

### Frontend Endpoints
- `GET /` - CRM Dashboard
- `GET /api/contacts` - Get all contacts
- `GET /api/messages/<phone>` - Get messages for contact
- `POST /api/send-message` - Send message to contact

### Webhook Endpoints
- `POST /webhook` - Receive WhatsApp messages
- `GET /webhook` - Webhook verification

## 📱 Usage Guide

### Viewing Conversations
1. Open the CRM dashboard
2. Browse contacts in the left sidebar
3. Click on any contact to view conversation history
4. Unread messages are highlighted with green badges

### Sending Messages
1. Select a contact from the sidebar
2. Type your message in the input field at the bottom
3. Press Enter or click the send button
4. Message will be sent via Tata WhatsApp API

### Managing Contacts
- Contacts are automatically created when they message you
- Contact information is updated from WhatsApp profile data
- Search contacts using the search bar

### AI Responses
- AI automatically responds to incoming messages
- Responses are contextual and conversational
- AI responses are marked as "sent" messages in the CRM

## 🔍 Troubleshooting

### Common Issues

**Messages not appearing in CRM**
- Check webhook configuration in Tata panel
- Verify webhook URL is accessible
- Check server logs for webhook errors

**Cannot send messages**
- Verify WHATSAPP_TOKEN in .env file
- Ensure contact has opted in to receive messages
- Check Tata API rate limits

**AI responses not working**
- Verify OPENAI_API_KEY in .env file
- Check OpenAI API quota and billing
- Review server logs for API errors

### Debug Mode
Run with debug logging:
```bash
python enhanced_crm.py
```

Check logs for detailed error information.

## 📈 Features Roadmap

### Planned Features
- [ ] Message templates management
- [ ] Bulk messaging
- [ ] Contact tagging and segmentation
- [ ] Analytics and reporting
- [ ] File/media message support
- [ ] Multi-agent support
- [ ] Integration with other CRM systems

### Advanced Features
- [ ] Chatbot flows and automation
- [ ] Integration with e-commerce platforms
- [ ] Advanced AI training with custom data
- [ ] Multi-language support
- [ ] Voice message support

## 🤝 Support

For support and questions:
1. Check the troubleshooting section
2. Review server logs for errors
3. Verify API credentials and configurations
4. Test webhook connectivity

## 📄 License

This project is for internal use with Tata Telecom WhatsApp Business API.

## 🔒 Security Notes

- Keep your API tokens secure
- Use HTTPS for webhook endpoints
- Regularly rotate API keys
- Monitor API usage and logs
- Implement proper access controls for production use

---

**Happy messaging! 📱💬**