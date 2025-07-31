from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# In-memory storage (use database in production)
chats = {}
ai_enabled_chats = set()

def fetch_recent_chats():
    """Fetch recent conversations from Tata Telecom WhatsApp API"""
    try:
        # Use proper Tata Telecom API endpoints
        headers = {
            'Authorization': WHATSAPP_TOKEN,  # Direct token, not Bearer
            'Content-Type': 'application/json'
        }
        
        # Try to get phone number settings first to verify connection
        settings_url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/settings"
        print(f"Testing API connection with settings endpoint...")
        
        response = requests.get(settings_url, headers=headers)
        print(f"Settings API Response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            print("API connection successful")
            
            # Since there's no direct conversation history endpoint in Tata API,
            # we'll need to rely on webhook data and stored conversations
            # For now, let's check if we have any stored chats
            if not chats:
                print("No existing chats found. Chats will appear when messages are received via webhook.")
                print("Make sure your webhook is configured at: https://your-domain.com/webhook")
                return True
            else:
                print(f"Found {len(chats)} existing chats")
                return True
        else:
            print(f"API connection failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error connecting to Tata Telecom API: {e}")
        return False

def get_phone_settings():
    """Get WhatsApp phone number settings to verify API connection"""
    try:
        url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/settings"
        headers = {
            'Authorization': WHATSAPP_TOKEN,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            settings = response.json()
            print(f"Phone settings: {json.dumps(settings, indent=2)}")
            return settings
        else:
            print(f"Failed to get settings: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error getting phone settings: {e}")
        return None

@app.route('/')
def dashboard():
    # Test API connection and fetch recent chats when dashboard loads
    fetch_recent_chats()
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/test-connection')
def test_connection():
    """Test API connection and return status"""
    settings = get_phone_settings()
    return jsonify({
        'connected': settings is not None,
        'settings': settings,
        'chat_count': len(chats)
    })

@app.route('/api/refresh-chats', methods=['POST'])
def refresh_chats():
    """Manually refresh chats from API"""
    success = fetch_recent_chats()
    return jsonify({'success': success, 'count': len(chats)})

@app.route('/api/chats')
def get_chats():
    return jsonify({
        'chats': chats,
        'ai_enabled': list(ai_enabled_chats)
    })

@app.route('/api/send', methods=['POST'])
def send_manual_message():
    try:
        data = request.json
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({'success': False, 'error': 'Phone and message required'})
        
        success = send_whatsapp_message(phone, message)
        if success:
            add_message(phone, message, 'sent', 'manual')
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to send message'})
    except Exception as e:
        print(f"Error in send_manual_message: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/toggle-ai', methods=['POST'])
def toggle_ai():
    data = request.json
    phone = data.get('phone')
    
    if phone in ai_enabled_chats:
        ai_enabled_chats.remove(phone)
        status = 'disabled'
    else:
        ai_enabled_chats.add(phone)
        status = 'enabled'
    
    return jsonify({'success': True, 'status': status})

@app.route('/api/add-contact', methods=['POST'])
def add_contact():
    data = request.json
    phone = data.get('phone')
    
    if phone and phone not in chats:
        chats[phone] = []
        add_message(phone, "Contact added for testing", 'received', 'system')
    
    return jsonify({'success': True})

@app.route('/api/simulate-message', methods=['POST'])
def simulate_message():
    data = request.json
    phone = data.get('phone')
    message = data.get('message')
    
    if phone and message:
        add_message(phone, message, 'received')
        
        # Auto-reply if AI is enabled
        if phone in ai_enabled_chats:
            ai_response = get_ai_response(message)
            add_message(phone, ai_response, 'sent', 'ai')
    
    return jsonify({'success': True})

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
    
    # Extract message from Tata Telecom format
    phone = extract_phone(data)
    message_text = extract_message(data)
    
    print(f"Extracted - Phone: {phone}, Message: {message_text}")
    
    if phone and message_text:
        add_message(phone, message_text, 'received')
        print(f"Message added to chat for {phone}")
        
        # Auto-reply if AI is enabled for this chat
        if phone in ai_enabled_chats:
            print(f"AI enabled for {phone}, generating response...")
            ai_response = get_ai_response(message_text)
            if send_whatsapp_message(phone, ai_response):
                add_message(phone, ai_response, 'sent', 'ai')
                print(f"AI response sent: {ai_response}")
    else:
        print("Could not extract phone/message from webhook data")
    
    return jsonify({'status': 'success'})

def extract_phone(data):
    # Handle Tata Telecom webhook format from the API docs
    # Format: {"messages": {"from": "919999999999", ...}}
    if data.get('messages'):
        return data.get('messages', {}).get('from')
    # Format: {"contacts": [{"wa_id": "919999999999"}]}
    if data.get('contacts'):
        contacts = data.get('contacts', [])
        if contacts and len(contacts) > 0:
            return contacts[0].get('wa_id')
    # Direct format: {"from": "919999999999"}
    return data.get('from')

def extract_message(data):
    # Handle Tata Telecom webhook format from the API docs
    # Format: {"messages": {"text": {"body": "message"}, "type": "text"}}
    if data.get('messages'):
        msg = data.get('messages', {})
        if msg.get('text') and msg.get('text', {}).get('body'):
            return msg.get('text', {}).get('body')
    # Direct format for testing
    if data.get('text') and data.get('text', {}).get('body'):
        return data.get('text', {}).get('body')
    return None

def add_message(phone, message, direction, source='user'):
    if phone not in chats:
        chats[phone] = []
    
    chats[phone].append({
        'message': message,
        'direction': direction,
        'source': source,
        'timestamp': datetime.now().isoformat()
    })

def get_ai_response(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful WhatsApp assistant. Keep responses brief and friendly."},
                {"role": "user", "content": message}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except:
        return "Sorry, I'm having trouble responding right now."

def send_whatsapp_message(to, message):
    """Send WhatsApp message using Tata Telecom API"""
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    
    # Correct headers format for Tata Telecom API
    headers = {
        'Authorization': WHATSAPP_TOKEN,  # Direct token, not Bearer
        'Content-Type': 'application/json'
    }
    
    # Correct payload format based on API docs
    payload = {
        "to": to,
        "type": "text",
        "source": "external",
        "text": {
            "body": message
        }
    }
    
    try:
        print(f"Sending message to {to}: {message}")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        # Check for success
        if response.status_code == 200:
            try:
                if response.text.strip():
                    response_data = response.json()
                    if response_data.get('id'):
                        print(f"Message sent successfully, ID: {response_data.get('id')}")
                        return True
                else:
                    print("Empty response but status 200 - considering success")
                    return True
            except json.JSONDecodeError:
                print(f"Non-JSON response: {response.text[:100]}")  
                return response.status_code == 200
        
        # Handle different error responses
        if response.status_code == 401:
            print("Authentication failed - check your WHATSAPP_TOKEN")
        elif response.status_code == 400:
            print("Bad request - check message format")
        elif response.status_code == 424:
            print("WhatsApp API error - check phone number permissions")
        
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"Network error sending message: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error sending message: {e}")
        return False

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Chat Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #25d366; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .chat-list { display: grid; grid-template-columns: 300px 1fr; gap: 20px; }
        .contacts { background: white; border-radius: 8px; padding: 20px; height: 600px; overflow-y: auto; }
        .chat-area { background: white; border-radius: 8px; padding: 20px; height: 600px; display: flex; flex-direction: column; }
        .contact { padding: 15px; border-bottom: 1px solid #eee; cursor: pointer; }
        .contact:hover { background: #f0f0f0; }
        .contact.active { background: #e3f2fd; }
        .messages { flex: 1; overflow-y: auto; padding: 10px; border: 1px solid #eee; margin-bottom: 10px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; max-width: 70%; }
        .received { background: #f1f1f1; align-self: flex-start; }
        .sent { background: #dcf8c6; align-self: flex-end; margin-left: auto; }
        .ai-badge { background: #2196f3; color: white; font-size: 10px; padding: 2px 6px; border-radius: 10px; }
        .controls { display: flex; gap: 10px; margin-bottom: 10px; }
        .input-area { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .send-btn { background: #25d366; color: white; }
        .ai-btn { background: #2196f3; color: white; }
        .ai-btn.enabled { background: #4caf50; }
        .timestamp { font-size: 10px; color: #666; margin-top: 5px; }

    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>WhatsApp Chat Manager</h1>
            <p>Manage chats manually or assign to AI</p>
        </div>
        

        
        <div class="chat-list">
            <div class="contacts">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3>Contacts</h3>
                    <div>
                        <button onclick="testConnection()" style="padding: 5px 10px; background: #2196f3; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 5px;">Test API</button>
                        <button onclick="refreshChats()" style="padding: 5px 10px; background: #25d366; color: white; border: none; border-radius: 4px; cursor: pointer;">Refresh</button>
                    </div>
                </div>
                <div id="apiStatus" style="padding: 10px; margin-bottom: 10px; border-radius: 4px; font-size: 12px;"></div>
                <div id="contactList"></div>
            </div>
            
            <div class="chat-area">
                <div class="controls">
                    <button id="aiToggle" class="ai-btn" onclick="toggleAI()">AI: Disabled</button>
                    <span id="currentContact">Select a contact</span>
                </div>
                
                <div id="messages" class="messages"></div>
                
                <div class="input-area">
                    <input type="text" id="messageInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                    <button class="send-btn" onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentPhone = null;
        let chats = {};
        let aiEnabled = [];

        function loadChats() {
            fetch('/api/chats')
                .then(r => r.json())
                .then(data => {
                    chats = data.chats;
                    aiEnabled = data.ai_enabled;
                    updateContactList();
                    if (currentPhone) updateMessages();
                });
        }

        function updateContactList() {
            const list = document.getElementById('contactList');
            list.innerHTML = '';
            
            Object.keys(chats).forEach(phone => {
                const div = document.createElement('div');
                div.className = 'contact' + (phone === currentPhone ? ' active' : '');
                div.onclick = () => selectContact(phone);
                
                const lastMsg = chats[phone][chats[phone].length - 1];
                const isAI = aiEnabled.includes(phone);
                
                div.innerHTML = `
                    <strong>${phone}</strong>
                    ${isAI ? '<span class="ai-badge">AI</span>' : ''}
                    <div style="font-size: 12px; color: #666; margin-top: 5px;">
                        ${lastMsg.message.substring(0, 50)}...
                    </div>
                `;
                list.appendChild(div);
            });
        }

        function selectContact(phone) {
            currentPhone = phone;
            document.getElementById('currentContact').textContent = phone;
            
            const aiBtn = document.getElementById('aiToggle');
            const isEnabled = aiEnabled.includes(phone);
            aiBtn.textContent = 'AI: ' + (isEnabled ? 'Enabled' : 'Disabled');
            aiBtn.className = 'ai-btn' + (isEnabled ? ' enabled' : '');
            
            updateContactList();
            updateMessages();
        }

        function updateMessages() {
            if (!currentPhone || !chats[currentPhone]) return;
            
            const container = document.getElementById('messages');
            container.innerHTML = '';
            
            chats[currentPhone].forEach(msg => {
                const div = document.createElement('div');
                div.className = 'message ' + msg.direction;
                
                let badge = '';
                if (msg.source === 'ai') badge = '<span class="ai-badge">AI</span> ';
                if (msg.source === 'manual') badge = '<span style="background:#ff9800;color:white;font-size:10px;padding:2px 6px;border-radius:10px;">Manual</span> ';
                
                div.innerHTML = `
                    ${badge}${msg.message}
                    <div class="timestamp">${new Date(msg.timestamp).toLocaleTimeString()}</div>
                `;
                container.appendChild(div);
            });
            
            container.scrollTop = container.scrollHeight;
        }

        function sendMessage() {
            if (!currentPhone) return;
            
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            fetch('/api/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone: currentPhone, message})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    input.value = '';
                    loadChats();
                }
            });
        }

        function toggleAI() {
            if (!currentPhone) return;
            
            fetch('/api/toggle-ai', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone: currentPhone})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    loadChats();
                }
            });
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function refreshChats() {
            fetch('/api/refresh-chats', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(r => r.json())
            .then(data => {
                console.log(`Refreshed ${data.count} chats`);
                loadChats();
            })
            .catch(err => console.error('Error refreshing chats:', err));
        }

        function testConnection() {
            const statusDiv = document.getElementById('apiStatus');
            statusDiv.innerHTML = 'Testing API connection...';
            statusDiv.style.background = '#fff3cd';
            
            fetch('/api/test-connection')
            .then(r => r.json())
            .then(data => {
                if (data.connected) {
                    statusDiv.innerHTML = `API Connected - ${data.chat_count} chats loaded`;
                    statusDiv.style.background = '#d4edda';
                } else {
                    statusDiv.innerHTML = 'API Connection Failed - Check your token';
                    statusDiv.style.background = '#f8d7da';
                }
                console.log('API Status:', data);
            })
            .catch(err => {
                statusDiv.innerHTML = 'Connection Error';
                statusDiv.style.background = '#f8d7da';
                console.error('Connection test failed:', err);
            });
        }

        // Load chats every 5 seconds
        setInterval(loadChats, 5000);
        loadChats();
        
        // Test API connection on page load
        setTimeout(testConnection, 1000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)