from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# In-memory storage
chats_db = {}
messages_db = {}

@app.route('/')
def dashboard():
    return send_from_directory('static', 'dashboard.html')

@app.route('/api/chats', methods=['GET'])
def get_chats():
    # Fetch chats from Tata API
    try:
        headers = {
            'Authorization': f'Bearer {WHATSAPP_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Get conversations from Tata API
        response = requests.get('https://wb.omni.tatatelebusiness.com/conversations', headers=headers)
        
        if response.status_code == 200:
            tata_chats = response.json()
            chat_list = []
            
            for chat in tata_chats.get('conversations', []):
                chat_list.append({
                    'phone': chat.get('contact', {}).get('phone', 'Unknown'),
                    'lastMessage': chat.get('lastMessage', {}).get('text', 'No messages'),
                    'timestamp': chat.get('updatedAt', ''),
                    'messageCount': chat.get('messageCount', 0)
                })
        else:
            # Fallback to local storage
            chat_list = []
            for phone, chat_data in chats_db.items():
                chat_list.append({
                    'phone': phone,
                    'lastMessage': chat_data.get('lastMessage', 'No messages'),
                    'timestamp': chat_data.get('timestamp', ''),
                    'messageCount': len(messages_db.get(phone, []))
                })
    
    except Exception as e:
        print(f"Error fetching chats: {e}")
        # Fallback to local storage
        chat_list = []
        for phone, chat_data in chats_db.items():
            chat_list.append({
                'phone': phone,
                'lastMessage': chat_data.get('lastMessage', 'No messages'),
                'timestamp': chat_data.get('timestamp', ''),
                'messageCount': len(messages_db.get(phone, []))
            })
    
    stats = {
        'totalMessages': sum(len(msgs) for msgs in messages_db.values()),
        'activeChats': len(chat_list),
        'aiResponses': sum(1 for msgs in messages_db.values() for msg in msgs if msg.get('type') == 'sent'),
        'successRate': 95
    }
    
    return jsonify({'chats': chat_list, 'stats': stats})

@app.route('/api/send-message', methods=['POST'])
def api_send_message():
    data = request.get_json()
    phone = data.get('phone')
    message = data.get('message')
    
    if not phone or not message:
        return jsonify({'success': False, 'error': 'Phone and message required'})
    
    # Send session message using Tata API
    success = send_session_message(phone, message)
    
    if success:
        # Store message locally
        if phone not in messages_db:
            messages_db[phone] = []
        
        messages_db[phone].append({
            'text': message,
            'type': 'sent',
            'timestamp': datetime.now().isoformat()
        })
        
        chats_db[phone] = {
            'lastMessage': message,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to send message. User must message you first for session messages.'})

@app.route('/api/send-template', methods=['POST'])
def api_send_template():
    data = request.get_json()
    phone = data.get('phone')
    
    if not phone:
        return jsonify({'success': False, 'error': 'Phone number required'})
    
    # Send template message using Tata API
    success = send_template_message(phone)
    
    if success:
        # Store template message locally
        if phone not in messages_db:
            messages_db[phone] = []
        
        template_msg = "Welcome template sent"
        messages_db[phone].append({
            'text': template_msg,
            'type': 'sent',
            'timestamp': datetime.now().isoformat()
        })
        
        chats_db[phone] = {
            'lastMessage': template_msg,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({'success': True, 'message': 'Template message sent! User can now reply.'})
    else:
        return jsonify({'success': False, 'error': 'Failed to send template message'})

def send_session_message(phone, message):
    """Send session message using Tata API"""
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'to': phone,
        'type': 'text',
        'source': 'external',
        'text': {'body': message},
        'metaData': {'custom_callback_data': 'session_message'}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Session message response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending session message: {e}")
        return False

def send_template_message(phone):
    """Send template message using Tata API"""
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Use hello_world template (default WhatsApp template)
    payload = {
        'to': phone,
        'type': 'template',
        'template': {
            'name': 'hello_world',
            'language': {'code': 'en_US'}
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Template message response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            return True
        else:
            # If template fails, try session message as fallback
            print("Template failed, trying session message...")
            return send_session_message(phone, "Hello! Welcome to our AI assistant. Reply with any message to start chatting. 🤖")
            
    except Exception as e:
        print(f"Error sending template message: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print(f"Received webhook data: {data}")
    
    # Handle Tata webhook format
    if data.get('messages'):
        message_data = data['messages']
        phone = message_data.get('from')
        
        if message_data.get('text'):
            message_text = message_data['text'].get('body')
        else:
            message_text = None
            
    else:
        # Alternative format
        phone = data.get('from')
        if data.get('text'):
            message_text = data['text'].get('body') if isinstance(data['text'], dict) else data['text']
        else:
            message_text = data.get('message')
    
    if phone and message_text:
        print(f"Processing message from {phone}: {message_text}")
        
        # Store received message
        if phone not in messages_db:
            messages_db[phone] = []
        
        messages_db[phone].append({
            'text': message_text,
            'type': 'received',
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            # Get AI response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful WhatsApp assistant. Keep responses brief and friendly."},
                    {"role": "user", "content": message_text}
                ],
                max_tokens=150
            )
            
            ai_response = response.choices[0].message.content
            print(f"AI Response: {ai_response}")
            
            # Send AI reply
            success = send_session_message(phone, ai_response)
            
            if success:
                # Store AI response
                messages_db[phone].append({
                    'text': ai_response,
                    'type': 'sent',
                    'timestamp': datetime.now().isoformat()
                })
                
                chats_db[phone] = {
                    'lastMessage': message_text,
                    'timestamp': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            error_msg = "Sorry, I encountered an error. Please try again."
            send_session_message(phone, error_msg)
    
    return jsonify({'status': 'success', 'message': 'received'})

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == os.getenv('VERIFY_TOKEN'):
        return challenge
    return 'Forbidden', 403

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)