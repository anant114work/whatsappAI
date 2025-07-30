from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage
chats = {}
ai_enabled_chats = set()

@app.route('/')
def dashboard():
    return render_template_string(SIMPLE_HTML)

@app.route('/api/chats')
def get_chats():
    return jsonify({
        'chats': chats,
        'ai_enabled': list(ai_enabled_chats)
    })

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == 'tata_webhook_verify_2024':
        return challenge
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.get_json()
        print(f"Webhook received: {json.dumps(data, indent=2)}")
        
        # Extract phone and message
        phone = None
        message_text = None
        
        # Try messages format
        if data.get('messages'):
            phone = data.get('messages', {}).get('from')
            msg = data.get('messages', {})
            if msg.get('text'):
                message_text = msg.get('text', {}).get('body')
        
        # Try contacts format if no phone found
        if not phone and data.get('contacts'):
            contacts = data.get('contacts', [])
            if contacts:
                phone = contacts[0].get('wa_id')
        
        print(f"Extracted - Phone: {phone}, Message: {message_text}")
        
        if phone and message_text:
            # Add to chats
            if phone not in chats:
                chats[phone] = []
            
            chats[phone].append({
                'message': message_text,
                'direction': 'received',
                'source': 'user',
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"Message added to chat for {phone}")
            return jsonify({'status': 'success', 'message': 'Message received'})
        else:
            print("Could not extract phone/message")
            return jsonify({'status': 'error', 'message': 'Could not extract data'})
            
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

SIMPLE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple WhatsApp Chat Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chat { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 8px; }
        .message { margin: 5px 0; padding: 8px; background: #f0f0f0; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Simple WhatsApp Chat Manager</h1>
    <button onclick="loadChats()">Refresh Chats</button>
    <div id="chats"></div>

    <script>
        function loadChats() {
            fetch('/api/chats')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('chats');
                    container.innerHTML = '';
                    
                    Object.keys(data.chats).forEach(phone => {
                        const chatDiv = document.createElement('div');
                        chatDiv.className = 'chat';
                        chatDiv.innerHTML = `<h3>${phone}</h3>`;
                        
                        data.chats[phone].forEach(msg => {
                            const msgDiv = document.createElement('div');
                            msgDiv.className = 'message';
                            msgDiv.innerHTML = `${msg.message} <small>(${new Date(msg.timestamp).toLocaleTimeString()})</small>`;
                            chatDiv.appendChild(msgDiv);
                        });
                        
                        container.appendChild(chatDiv);
                    });
                    
                    if (Object.keys(data.chats).length === 0) {
                        container.innerHTML = '<p>No chats yet. Send a message to your WhatsApp number to test.</p>';
                    }
                });
        }
        
        // Auto-refresh every 3 seconds
        setInterval(loadChats, 3000);
        loadChats();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)