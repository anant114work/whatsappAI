from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

client = OpenAI(api_key=OPENAI_API_KEY)

# ONLY real data storage - NO sample data
real_conversations = {}
real_messages = {}

def send_whatsapp_message(phone, message):
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    headers = {'Authorization': f'Bearer {WHATSAPP_TOKEN}', 'Content-Type': 'application/json'}
    
    payload = {
        'to': phone,
        'type': 'text',
        'text': {'body': message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            # Store sent message as real data
            if phone not in real_messages:
                real_messages[phone] = []
            real_messages[phone].append({
                'text': message,
                'direction': 'sent',
                'timestamp': datetime.now().isoformat()
            })
            return True
    except:
        pass
    return False

@app.route('/')
def dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Real WhatsApp CRM - Zero Sample Data</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .container { display: flex; height: 100vh; }
        .sidebar { width: 350px; background: white; border-right: 1px solid #e0e0e0; display: flex; flex-direction: column; }
        .header { padding: 20px; background: #25d366; color: white; }
        .contacts-area { flex: 1; overflow-y: auto; }
        .chat-area { flex: 1; background: white; display: flex; flex-direction: column; }
        .empty-state { text-align: center; padding: 40px; color: #666; }
        .contact-item { padding: 15px; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
        .contact-item:hover { background: #f8f8f8; }
        .contact-item.active { background: #e3f2fd; }
        .messages-container { flex: 1; padding: 20px; overflow-y: auto; background: #f0f2f5; }
        .message { margin-bottom: 15px; display: flex; }
        .message.sent { justify-content: flex-end; }
        .message.received { justify-content: flex-start; }
        .message-bubble { max-width: 70%; padding: 12px 16px; border-radius: 18px; }
        .message.sent .message-bubble { background: #25d366; color: white; }
        .message.received .message-bubble { background: white; border: 1px solid #e0e0e0; }
        .input-area { padding: 20px; border-top: 1px solid #e0e0e0; display: flex; gap: 10px; }
        .message-input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 25px; outline: none; }
        .send-btn { background: #25d366; color: white; border: none; border-radius: 50%; width: 45px; height: 45px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="header">
                <h2>Real WhatsApp CRM</h2>
                <p>Only actual conversations</p>
            </div>
            <div class="contacts-area" id="contacts-area">
                <div class="empty-state">
                    <h3>No Real Conversations Yet</h3>
                    <p>Real conversations will appear here when:</p>
                    <ul style="text-align: left; margin-top: 10px;">
                        <li>Someone messages your WhatsApp number</li>
                        <li>Webhook receives actual messages</li>
                        <li>You send messages to real contacts</li>
                    </ul>
                    <p style="margin-top: 15px; font-size: 12px; color: #999;">
                        Zero sample data • Zero fake contacts • Only real chats
                    </p>
                </div>
            </div>
        </div>
        
        <div class="chat-area">
            <div id="empty-chat" class="empty-state" style="flex: 1;">
                <h3>Welcome to Real WhatsApp CRM</h3>
                <p>This system shows ONLY real conversations from your Tata WhatsApp Business</p>
                <br>
                <p><strong>No sample data included</strong></p>
                <p>When real users message you, they will appear in the sidebar</p>
                <br>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px;">
                    <p><strong>Send a test message:</strong></p>
                    <input type="text" id="test-phone" placeholder="+919999999999" style="width: 200px; padding: 8px; margin: 5px;">
                    <input type="text" id="test-message" placeholder="Test message" style="width: 200px; padding: 8px; margin: 5px;">
                    <button onclick="sendTestMessage()" style="padding: 8px 15px; background: #25d366; color: white; border: none; border-radius: 5px;">Send</button>
                </div>
            </div>
            
            <div id="chat-content" style="display: none; flex: 1; display: flex; flex-direction: column;">
                <div style="padding: 20px; border-bottom: 1px solid #e0e0e0; background: #f8f9fa;">
                    <h3 id="chat-contact-name">Contact</h3>
                    <p id="chat-contact-info">Real conversation</p>
                </div>
                
                <div class="messages-container" id="messages-container">
                    <!-- Real messages will appear here -->
                </div>
                
                <div class="input-area">
                    <input type="text" id="reply-input" class="message-input" placeholder="Type your reply..." onkeypress="handleKeyPress(event)">
                    <button class="send-btn" onclick="sendReply()">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentContact = null;

        async function loadRealContacts() {
            try {
                const response = await fetch('/api/real-contacts');
                const data = await response.json();
                
                const container = document.getElementById('contacts-area');
                
                if (data.contacts && data.contacts.length > 0) {
                    container.innerHTML = data.contacts.map(contact => `
                        <div class="contact-item" onclick="selectContact('${contact.phone}')">
                            <strong>${contact.name || contact.phone}</strong>
                            <p style="color: #666; font-size: 14px;">${contact.last_message}</p>
                            <small>${contact.message_count} real messages</small>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = `
                        <div class="empty-state">
                            <h3>No Real Conversations Yet</h3>
                            <p>Real conversations will appear here when:</p>
                            <ul style="text-align: left; margin-top: 10px;">
                                <li>Someone messages your WhatsApp number</li>
                                <li>Webhook receives actual messages</li>
                                <li>You send messages to real contacts</li>
                            </ul>
                            <p style="margin-top: 15px; font-size: 12px; color: #999;">
                                Zero sample data • Zero fake contacts • Only real chats
                            </p>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error loading contacts:', error);
            }
        }

        function selectContact(phone) {
            currentContact = phone;
            
            document.querySelectorAll('.contact-item').forEach(item => {
                item.classList.remove('active');
            });
            event.currentTarget.classList.add('active');
            
            document.getElementById('empty-chat').style.display = 'none';
            document.getElementById('chat-content').style.display = 'flex';
            
            document.getElementById('chat-contact-name').textContent = phone;
            document.getElementById('chat-contact-info').textContent = 'Real conversation from Tata WhatsApp';
            
            loadRealMessages(phone);
        }

        async function loadRealMessages(phone) {
            try {
                const response = await fetch(`/api/real-messages/${encodeURIComponent(phone)}`);
                const data = await response.json();
                
                const container = document.getElementById('messages-container');
                
                if (data.messages && data.messages.length > 0) {
                    container.innerHTML = data.messages.map(msg => `
                        <div class="message ${msg.direction}">
                            <div class="message-bubble">
                                <div>${msg.text}</div>
                                <div style="font-size: 11px; opacity: 0.7; margin-top: 5px;">${new Date(msg.timestamp).toLocaleString()}</div>
                            </div>
                        </div>
                    `).join('');
                    container.scrollTop = container.scrollHeight;
                } else {
                    container.innerHTML = '<div style="text-align: center; color: #666; padding: 20px;">No real message history found</div>';
                }
            } catch (error) {
                console.error('Error loading messages:', error);
            }
        }

        async function sendReply() {
            const input = document.getElementById('reply-input');
            const message = input.value.trim();
            
            if (!message || !currentContact) return;
            
            try {
                const response = await fetch('/api/send-real-message', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone: currentContact, message })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    input.value = '';
                    loadRealMessages(currentContact);
                    loadRealContacts();
                    alert('Real message sent via Tata API!');
                } else {
                    alert('Failed to send: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function sendTestMessage() {
            const phone = document.getElementById('test-phone').value;
            const message = document.getElementById('test-message').value;
            
            if (!phone || !message) {
                alert('Enter phone and message');
                return;
            }
            
            try {
                const response = await fetch('/api/send-real-message', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone, message })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('test-phone').value = '';
                    document.getElementById('test-message').value = '';
                    loadRealContacts();
                    alert('Test message sent! This will create a real conversation.');
                } else {
                    alert('Failed: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendReply();
            }
        }

        // Load real contacts every 10 seconds
        setInterval(loadRealContacts, 10000);
        loadRealContacts();
    </script>
</body>
</html>
    ''')

@app.route('/api/real-contacts')
def get_real_contacts():
    contacts = []
    for phone, messages in real_messages.items():
        if messages:  # Only show contacts with real messages
            last_message = messages[-1]['text'] if messages else 'No messages'
            contacts.append({
                'phone': phone,
                'name': real_conversations.get(phone, {}).get('name', 'Real User'),
                'last_message': last_message,
                'message_count': len(messages)
            })
    
    return jsonify({'contacts': contacts})

@app.route('/api/real-messages/<phone>')
def get_real_messages(phone):
    messages = real_messages.get(phone, [])
    return jsonify({'messages': messages})

@app.route('/api/send-real-message', methods=['POST'])
def send_real_message():
    data = request.get_json()
    phone = data.get('phone')
    message = data.get('message')
    
    if not phone or not message:
        return jsonify({'success': False, 'error': 'Phone and message required'})
    
    success = send_whatsapp_message(phone, message)
    
    if success:
        # Ensure contact exists in real conversations
        if phone not in real_conversations:
            real_conversations[phone] = {'name': 'Real User', 'phone': phone}
        
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to send via Tata API'})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Real webhook received: {json.dumps(data, indent=2)}")
    
    try:
        # Handle real incoming messages only
        phone = data.get('from')
        message_text = data.get('text', {}).get('body') if isinstance(data.get('text'), dict) else data.get('text')
        
        if phone and message_text:
            # Store as real conversation
            real_conversations[phone] = {
                'name': 'Real User',
                'phone': phone
            }
            
            # Store real message
            if phone not in real_messages:
                real_messages[phone] = []
            
            real_messages[phone].append({
                'text': message_text,
                'direction': 'received',
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"Stored real message from {phone}: {message_text}")
            
            # Generate AI response for real conversation
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful WhatsApp assistant. Keep responses brief and friendly."},
                        {"role": "user", "content": message_text}
                    ],
                    max_tokens=150
                )
                
                ai_response = response.choices[0].message.content
                send_whatsapp_message(phone, ai_response)
                print(f"Sent AI response to {phone}: {ai_response}")
                
            except Exception as e:
                print(f"AI response error: {e}")
    
    except Exception as e:
        print(f"Webhook processing error: {e}")
    
    return jsonify({'status': 'success', 'message': 'received'})

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge
    return 'Forbidden', 403

if __name__ == '__main__':
    print("Starting Real WhatsApp CRM - ZERO sample data")
    print("Only real conversations will be shown")
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)