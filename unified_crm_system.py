from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

# Unified message storage
conversations = {}



@app.route('/')
def crm_dashboard():
    return render_template_string(CRM_HTML)

@app.route('/api/conversations')
def get_conversations():
    print(f"API call: returning {len(conversations)} conversations")
    return jsonify({'conversations': conversations})

@app.route('/api/test-webhook', methods=['POST'])
def test_webhook():
    """Test endpoint to simulate incoming messages"""
    data = request.json
    platform = data.get('platform', 'whatsapp')
    phone = data.get('phone', '+919999999999')
    message = data.get('message', 'Test message')
    
    add_message(phone, message, 'received', platform, 'customer')
    print(f"Test message added: {phone} via {platform}")
    
    return jsonify({'success': True, 'message': 'Test message added'})

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json
    phone = data.get('phone')
    message = data.get('message')
    
    if not phone or not message:
        return jsonify({'success': False, 'error': 'Phone and message required'})
    
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "to": phone,
        "type": "text",
        "source": "crm",
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            add_message(phone, message, 'sent', 'whatsapp', 'agent')
            return jsonify({'success': True, 'message': 'Message sent via Tata WhatsApp API'})
        return jsonify({'success': False, 'error': f'Tata API error: {response.text}'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Send failed: {str(e)}'})



# WhatsApp Webhook
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print(f"Webhook received: {json.dumps(data, indent=2)}")
    
    try:
        # Handle different Tata webhook formats
        phone = None
        message = None
        
        # Format 1: Standard Tata format
        if data.get('contacts') and data.get('messages'):
            phone = data['contacts'][0]['wa_id']
            message_data = data['messages']
            if message_data.get('text'):
                message = message_data['text']['body']
        
        # Format 2: Direct format
        elif data.get('from') and data.get('text'):
            phone = data['from']
            message = data['text'].get('body') if isinstance(data['text'], dict) else data['text']
        
        # Format 3: Messages array
        elif data.get('messages'):
            msg_data = data['messages']
            phone = msg_data.get('from')
            if msg_data.get('text'):
                message = msg_data['text'].get('body')
        
        if phone and message:
            add_message(phone, message, 'received', 'whatsapp', 'customer')
            print(f"Real message added: {phone} - {message}")
            
    except Exception as e:
        print(f"Webhook error: {e}")
    
    return jsonify({'status': 'success'})

# RCS Webhook
@app.route('/webhook/rcs', methods=['POST'])
def handle_rcs_webhook():
    data = request.get_json()
    print(f"RCS webhook: {json.dumps(data, indent=2)}")
    
    # Extract RCS message
    if data.get('entityType') == 'USER_MESSAGE':
        phone = data.get('userPhoneNumber')
        entity = data.get('entity', {})
        message = entity.get('text')
        
        if phone and message:
            add_message(phone, message, 'received', 'rcs', 'customer')
    
    return jsonify({'status': 'success'})

def add_message(phone, message, direction, platform, sender_type):
    if phone not in conversations:
        conversations[phone] = {
            'contact': phone,
            'messages': [],
            'last_activity': datetime.now().isoformat(),
            'platforms': set()
        }
    
    conversations[phone]['messages'].append({
        'message': message,
        'direction': direction,
        'platform': platform,
        'sender_type': sender_type,
        'timestamp': datetime.now().isoformat()
    })
    
    conversations[phone]['platforms'].add(platform)
    conversations[phone]['last_activity'] = datetime.now().isoformat()
    conversations[phone]['platforms'] = list(conversations[phone]['platforms'])
    
    print(f"Message added: {phone} ({platform}) - {message[:50]}...")

CRM_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Unified CRM - WhatsApp & RCS</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { background: #25d366; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .main-layout { display: grid; grid-template-columns: 350px 1fr; gap: 20px; }
        .contacts-panel { background: white; border-radius: 8px; padding: 20px; height: 700px; overflow-y: auto; }
        .chat-panel { background: white; border-radius: 8px; padding: 20px; height: 700px; display: flex; flex-direction: column; }
        .contact { padding: 15px; border-bottom: 1px solid #eee; cursor: pointer; }
        .contact:hover { background: #f0f0f0; }
        .contact.active { background: #e3f2fd; }
        .platform-badge { font-size: 10px; padding: 2px 6px; border-radius: 10px; margin-left: 5px; }
        .whatsapp { background: #25d366; color: white; }
        .rcs { background: #1976d2; color: white; }
        .messages { flex: 1; overflow-y: auto; padding: 10px; border: 1px solid #eee; margin-bottom: 15px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; max-width: 70%; }
        .received { background: #f1f1f1; align-self: flex-start; }
        .sent { background: #dcf8c6; align-self: flex-end; margin-left: auto; }
        .message-header { font-size: 10px; color: #666; margin-bottom: 5px; }
        .reply-area { display: flex; gap: 10px; }
        .reply-input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .send-btn { padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; color: white; }
        .whatsapp-btn { background: #25d366; }
        .rcs-btn { background: #1976d2; }
        .contact-info { margin-bottom: 15px; padding: 10px; background: #f8f9fa; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Unified CRM - WhatsApp & RCS Messages</h1>
            <p>Manage all customer conversations in one place</p>
        </div>
        
        <div class="main-layout">
            <div class="contacts-panel">
                <h3>Conversations</h3>
                <button onclick="loadConversations()" style="margin-bottom: 10px; padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Refresh</button>
                <button onclick="addTestMessage()" style="margin-bottom: 15px; padding: 8px 15px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">Add Test Message</button>
                <div id="contactsList"></div>
            </div>
            
            <div class="chat-panel">
                <div class="contact-info" id="contactInfo" style="display: none;">
                    <strong id="currentContact">Select a conversation</strong>
                    <div id="platformInfo"></div>
                </div>
                
                <div id="messages" class="messages">
                    <p style="text-align: center; color: #666;">Select a conversation to view messages</p>
                </div>
                
                <div class="reply-area">
                    <input type="text" id="replyInput" class="reply-input" placeholder="Type your reply..." onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()" class="send-btn whatsapp-btn">Send via Tata WhatsApp</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentContact = null;
        let conversations = {};

        function loadConversations() {
            fetch('/api/conversations')
                .then(r => r.json())
                .then(data => {
                    conversations = data.conversations;
                    displayContacts();
                });
        }

        function displayContacts() {
            const container = document.getElementById('contactsList');
            container.innerHTML = '';
            
            if (Object.keys(conversations).length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">No conversations yet.<br>Click "Add Test Message" to see how it works!</p>';
                return;
            }
            
            Object.keys(conversations).forEach(phone => {
                const conv = conversations[phone];
                const div = document.createElement('div');
                div.className = 'contact' + (phone === currentContact ? ' active' : '');
                div.onclick = () => selectContact(phone);
                
                const lastMsg = conv.messages[conv.messages.length - 1];
                const platformBadges = conv.platforms.map(p => 
                    `<span class="platform-badge ${p}">${p.toUpperCase()}</span>`
                ).join('');
                
                div.innerHTML = `
                    <strong>${phone}</strong>
                    ${platformBadges}
                    <div style="font-size: 12px; color: #666; margin-top: 5px;">
                        ${lastMsg ? lastMsg.message.substring(0, 50) + '...' : 'No messages'}
                    </div>
                    <div style="font-size: 10px; color: #999;">
                        ${new Date(conv.last_activity).toLocaleString()}
                    </div>
                `;
                container.appendChild(div);
            });
        }

        function selectContact(phone) {
            currentContact = phone;
            const conv = conversations[phone];
            
            document.getElementById('contactInfo').style.display = 'block';
            document.getElementById('currentContact').textContent = phone;
            document.getElementById('platformInfo').innerHTML = 
                'Platforms: ' + conv.platforms.map(p => 
                    `<span class="platform-badge ${p}">${p.toUpperCase()}</span>`
                ).join(' ');
            
            // Enable reply input for selected contact
            document.getElementById('replyInput').disabled = false;
            document.getElementById('replyInput').placeholder = `Type message to ${phone}...`;
            
            displayMessages();
            displayContacts(); // Refresh to show active state
        }

        function displayMessages() {
            if (!currentContact) return;
            
            const container = document.getElementById('messages');
            container.innerHTML = '';
            
            const conv = conversations[currentContact];
            conv.messages.forEach(msg => {
                const div = document.createElement('div');
                div.className = 'message ' + msg.direction;
                
                div.innerHTML = `
                    <div class="message-header">
                        <span class="platform-badge ${msg.platform}">${msg.platform.toUpperCase()}</span>
                        ${msg.sender_type} • ${new Date(msg.timestamp).toLocaleTimeString()}
                    </div>
                    ${msg.message}
                `;
                container.appendChild(div);
            });
            
            container.scrollTop = container.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('replyInput');
            const message = input.value.trim();
            
            if (!message || !currentContact) return;
            
            fetch('/api/send-message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone: currentContact, message})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    input.value = '';
                    loadConversations();
                    alert('Message sent via Tata WhatsApp!');
                } else {
                    alert('Failed to send: ' + (data.error || 'Unknown error'));
                }
            });
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function addTestMessage() {
            const phone = '+91' + Math.floor(Math.random() * 9000000000 + 1000000000);
            const messages = [
                'Hello, I need help!',
                'What are your business hours?',
                'Can you help me with my order?',
                'I have a question about pricing',
                'Thank you for your service'
            ];
            const platforms = ['whatsapp', 'rcs'];
            
            const testData = {
                phone: phone,
                message: messages[Math.floor(Math.random() * messages.length)],
                platform: platforms[Math.floor(Math.random() * platforms.length)]
            };
            
            fetch('/api/test-webhook', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(testData)
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    loadConversations();
                }
            });
        }

        // Auto-refresh every 5 seconds
        setInterval(loadConversations, 5000);
        loadConversations();
        
        // Show initial status
        console.log('CRM Dashboard loaded');
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)