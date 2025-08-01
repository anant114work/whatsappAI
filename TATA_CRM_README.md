# 📱 Tata WhatsApp CRM - Real Data Only

A Customer Relationship Management system that connects directly to your Tata Telecom WhatsApp Business panel to display **ONLY REAL CONVERSATIONS** - no sample data, no fake chats.

## ✨ Key Features

### 🔄 Real-Time Tata Integration
- **Direct API Connection**: Connects to Tata WhatsApp Business API
- **Real Conversations Only**: Shows actual chats from your Tata panel
- **Historical Data**: Fetches all previous conversations going back years
- **Live Sync**: Real-time message updates via webhook

### 💬 Complete CRM Interface
- **WhatsApp-like UI**: Familiar chat interface
- **Contact Management**: All your real contacts in one place
- **Message History**: Complete conversation threads
- **Search & Filter**: Find any contact or conversation quickly

### 🤖 AI-Powered Responses
- **Auto-Reply**: AI responds to incoming messages automatically
- **Context Aware**: Understands conversation history
- **Manual Override**: Send custom replies anytime

### 📊 Real Analytics
- **Actual Message Counts**: Real statistics from your panel
- **Contact Activity**: See when customers last messaged
- **Response Tracking**: Monitor your reply rates

## 🚀 Quick Start

### 1. Initialize the CRM
```bash
python init_tata_crm.py
```

### 2. Start the CRM Server
```bash
python tata_crm.py
```

### 3. Open CRM Dashboard
Open: http://localhost:3000

### 4. Sync Your Real Data
Click **"Sync from Tata Panel"** to load all your actual conversations

## 🔧 Configuration

Your `.env` file should contain:
```env
WHATSAPP_TOKEN=your_actual_tata_token
OPENAI_API_KEY=your_openai_key
VERIFY_TOKEN=your_webhook_verify_token
```

## 📡 Webhook Setup

Configure your webhook URL in Tata panel:
```
https://whatsappai-x52i.onrender.com/webhook
```

This ensures new messages appear instantly in your CRM.

## 🎯 How It Works

### Data Sync Process
1. **API Connection**: CRM connects to Tata's WhatsApp Business API
2. **Conversation Fetch**: Retrieves all conversation threads
3. **Message History**: Downloads complete message history for each contact
4. **Real-Time Updates**: Webhook receives new messages instantly
5. **Database Storage**: Stores everything locally for fast access

### Supported Tata API Endpoints
The CRM automatically tries multiple endpoints to find your data:
- `/conversations` - Main conversation list
- `/whatsapp-cloud/conversations` - Cloud conversations
- `/api/conversations` - API conversations
- `/messages/{phone}` - Message history per contact

### Message Sending
- **Direct Integration**: Sends messages via Tata WhatsApp API
- **Status Tracking**: Monitors delivery status
- **Error Handling**: Graceful failure handling

## 📱 Using the CRM

### Viewing Conversations
1. Click "Sync from Tata Panel" to load real data
2. Browse your actual contacts in the left sidebar
3. Click any contact to view complete message history
4. All timestamps and message counts are real

### Sending Messages
1. Select a contact from your real conversation list
2. Type your message in the input field
3. Press Enter or click send
4. Message is sent via Tata API to the actual WhatsApp number

### AI Responses
- AI automatically replies to incoming messages
- Responses are contextual based on conversation history
- You can override AI responses anytime with manual replies

## 🔍 Troubleshooting

### "No contacts found" after sync
- **Check API Token**: Verify your WHATSAPP_TOKEN is correct
- **Panel Access**: Ensure you have access to Tata WhatsApp Business panel
- **API Permissions**: Confirm your token has conversation read permissions

### Messages not syncing
- **Webhook URL**: Verify webhook is configured in Tata panel
- **Network Access**: Ensure your server can reach Tata APIs
- **Token Validity**: Check if your API token has expired

### Cannot send messages
- **Contact Opt-in**: User must have messaged you first (WhatsApp policy)
- **API Limits**: Check if you've hit Tata API rate limits
- **Token Permissions**: Verify token has message send permissions

## 🔒 Data Privacy

- **Local Storage**: All data stored locally in SQLite database
- **No External Sharing**: Conversations never leave your system
- **Secure API**: Uses official Tata WhatsApp Business API
- **Token Security**: API tokens stored securely in environment variables

## 📊 Database Schema

### Contacts Table
```sql
- phone (TEXT): Contact phone number
- name (TEXT): Contact name from WhatsApp
- last_seen (DATETIME): Last activity timestamp
- total_messages (INTEGER): Total message count
- status (TEXT): Contact status
```

### Messages Table
```sql
- contact_phone (TEXT): Associated contact
- message_id (TEXT): Unique message ID from Tata
- message_text (TEXT): Message content
- message_type (TEXT): text/image/document/etc
- direction (TEXT): sent/received
- timestamp (DATETIME): Message timestamp
- status (TEXT): Message delivery status
```

## 🚀 Advanced Features

### Bulk Operations
- Export all conversations to CSV
- Bulk message sending (respecting WhatsApp policies)
- Contact tagging and segmentation

### Analytics Dashboard
- Message volume trends
- Response time analytics
- Customer engagement metrics
- Peak activity hours

### Integration Options
- Export to other CRM systems
- API endpoints for external integrations
- Webhook forwarding to other systems

## 🛠️ Development

### Adding Custom Features
The CRM is built with Flask and can be easily extended:

```python
@app.route('/api/custom-feature')
def custom_feature():
    # Your custom logic here
    return jsonify({'success': True})
```

### Database Queries
Access the SQLite database directly:

```python
conn = sqlite3.connect('tata_crm.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM contacts WHERE status = "active"')
results = cursor.fetchall()
```

## 📞 Support

### Common Issues
1. **Sync Failed**: Check API token and network connectivity
2. **No Messages**: Verify webhook configuration
3. **Send Failed**: Ensure contact has opted in by messaging first

### Debug Mode
Run with debug logging:
```bash
python tata_crm.py
```

Check console output for detailed error information.

## 🔄 Updates

### Keeping Data Fresh
- Manual sync: Click "Sync from Tata Panel" anytime
- Auto-sync: Webhook updates happen automatically
- Scheduled sync: Can be configured for periodic updates

### Backup Your Data
```bash
# Backup database
cp tata_crm.db tata_crm_backup.db

# Restore from backup
cp tata_crm_backup.db tata_crm.db
```

---

## 🎯 Summary

This CRM shows **ONLY REAL DATA** from your Tata WhatsApp Business panel:
- ✅ Real conversations from your panel
- ✅ Actual message history going back years  
- ✅ Real contact information
- ✅ Live message sync via webhook
- ❌ No sample data
- ❌ No fake conversations
- ❌ No dummy contacts

**Start using your real WhatsApp conversations in a professional CRM interface!**