# Complete Webhook Setup Guide for Unified CRM

## Overview
This guide will help you set up webhooks to receive ALL WhatsApp and RCS messages (new and previous) in your CRM system.

## Step 1: Start the Unified CRM System

```bash
python unified_crm_system.py
```

The system will be available at: `http://localhost:3000`

## Step 2: Expose Your Server (Required for Webhooks)

### Option A: Using ngrok (Recommended for testing)
```bash
# Install ngrok from https://ngrok.com/download
ngrok http 3000
```

This will give you URLs like:
- `https://abc123.ngrok.io` (use the HTTPS one)

### Option B: Deploy to cloud (Production)
Deploy to services like:
- Heroku
- AWS
- Google Cloud
- DigitalOcean

## Step 3: Configure WhatsApp Webhooks

### 3.1 Meta Business Manager Setup
1. Go to [business.facebook.com](https://business.facebook.com)
2. Select your WhatsApp Business Account
3. Navigate to **WhatsApp > Configuration**
4. In the **Webhook** section:
   - **Callback URL**: `https://your-domain.com/webhook/whatsapp`
   - **Verify Token**: `tata_webhook_verify_2024` (from your .env file)
   - Click **Verify and Save**
5. Subscribe to webhook fields:
   - ✅ **messages** (for incoming messages)
   - ✅ **message_deliveries** (for delivery status)
   - ✅ **message_reads** (for read receipts)

### 3.2 Test WhatsApp Webhook
Send a message to your WhatsApp Business number. You should see:
- Message appears in CRM dashboard
- Console logs showing webhook data

## Step 4: Configure RCS Webhooks

### 4.1 RCS Platform Setup
1. Access your RCS Business Messaging dashboard
2. Navigate to **Webhook Configuration**
3. Set webhook URLs:
   - **Message Webhook**: `https://your-domain.com/webhook/rcs`
   - **Callback Webhook**: `https://your-domain.com/webhook/rcs`

### 4.2 Test RCS Webhook
Send an RCS message to your business number to verify integration.

## Step 5: API Endpoints for Your CRM

### WhatsApp Message Sending
```http
POST /api/send-whatsapp
Content-Type: application/json

{
  "phone": "+919999999999",
  "message": "Hello from CRM"
}
```

### RCS Message Sending
```http
POST /api/send-rcs
Content-Type: application/json

{
  "phone": "+919999999999",
  "message": "Hello from CRM"
}
```

### Get All Conversations
```http
GET /api/conversations
```

## Step 6: Handling Previous Messages

### Important Note
The Tata Telecom APIs don't provide endpoints to retrieve historical messages. However, you can:

1. **Start Fresh**: Once webhooks are configured, all NEW messages will be captured
2. **Manual Import**: If you have message exports, create a script to import them
3. **Gradual Build**: Your message history will build up over time as customers interact

### Optional: Import Historical Data
If you have CSV/JSON exports of previous conversations:

```python
# Add this function to unified_crm_system.py
@app.route('/api/import-history', methods=['POST'])
def import_history():
    data = request.json
    for conversation in data.get('conversations', []):
        phone = conversation['phone']
        for msg in conversation['messages']:
            add_message(
                phone, 
                msg['text'], 
                msg['direction'], 
                msg['platform'], 
                msg['sender_type']
            )
    return jsonify({'success': True})
```

## Step 7: CRM Features

### Dashboard Features
- **Unified View**: All WhatsApp and RCS conversations in one place
- **Platform Badges**: Visual indicators showing which platforms each contact uses
- **Real-time Updates**: Messages appear instantly via webhooks
- **Multi-platform Reply**: Send replies via WhatsApp or RCS from the same interface

### Message Flow
1. **Incoming**: Customer sends message → Webhook → CRM displays message
2. **Outgoing**: Agent types reply → CRM → API call → Message sent to customer

## Step 8: Production Considerations

### Security
- Use HTTPS for all webhook URLs
- Validate webhook signatures (implement signature verification)
- Secure your AUTH_TOKEN

### Scalability
- Use a database instead of in-memory storage
- Implement message queuing for high volume
- Add error handling and retry logic

### Monitoring
- Log all webhook events
- Monitor API rate limits
- Set up alerts for failed message deliveries

## Troubleshooting

### Webhook Not Receiving Messages
1. Check if your server is accessible from the internet
2. Verify webhook URL is correct and uses HTTPS
3. Check webhook verification token matches
4. Look at server logs for errors

### Messages Not Sending
1. Verify AUTH_TOKEN is correct
2. Check phone number format (must include country code)
3. Ensure you have proper permissions for the phone number
4. Check API response for specific error messages

### Common Error Codes
- **401**: Invalid or expired AUTH_TOKEN
- **400**: Bad request format or invalid phone number
- **424**: WhatsApp/RCS API error (check permissions)

## Next Steps

1. **Start the system**: `python unified_crm_system.py`
2. **Expose with ngrok**: `ngrok http 3000`
3. **Configure webhooks** using the URLs provided
4. **Test with real messages**
5. **Monitor the dashboard** at `http://localhost:3000`

Your CRM will now capture all new WhatsApp and RCS messages in real-time and allow agents to reply from a unified interface!