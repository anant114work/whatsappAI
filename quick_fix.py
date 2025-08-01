from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Simple storage
chats_db = {}
messages_db = {}
all_contacts = {}

@app.route('/')
def dashboard():
    return send_from_directory('static', 'dashboard.html')

@app.route('/tata-chats')
def tata_chats_page():
    return send_from_directory('static', 'tata_chats.html')

@app.route('/api/import-contact', methods=['POST'])
def import_contact():
    data = request.get_json()
    phone = data.get('phone')
    name = data.get('name', 'Unknown')
    last_message = data.get('lastMessage', 'Imported contact')
    
    if not phone:
        return jsonify({'success': False, 'error': 'Phone required'})
    
    # Add to storage
    all_contacts[phone] = {
        'phone': phone,
        'name': name,
        'last_seen': datetime.now().isoformat(),
        'total_interactions': 1
    }
    
    chats_db[phone] = {
        'lastMessage': last_message,
        'timestamp': datetime.now().isoformat()
    }
    
    if phone not in messages_db:
        messages_db[phone] = []
    
    messages_db[phone].append({
        'text': last_message,
        'type': 'received',
        'timestamp': datetime.now().isoformat()
    })
    
    print(f"Imported contact: {phone} - {name}")
    return jsonify({'success': True, 'message': f'Contact {phone} imported'})

@app.route('/api/tata-chats', methods=['GET'])
def get_tata_chats():
    all_chats = []
    
    for phone, contact_info in all_contacts.items():
        messages = messages_db.get(phone, [])
        last_message = messages[-1] if messages else {'text': 'No messages', 'timestamp': ''}
        
        all_chats.append({
            'phone': phone,
            'name': contact_info.get('name', 'Unknown'),
            'lastMessage': last_message.get('text', 'No messages'),
            'timestamp': contact_info.get('last_seen', ''),
            'status': 'Active',
            'messageCount': len(messages),
            'totalInteractions': contact_info.get('total_interactions', 0)
        })
    
    return jsonify({
        'success': True,
        'chats': all_chats,
        'total': len(all_chats)
    })

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    phone = data.get('phone')
    message = data.get('message')
    
    if not phone or not message:
        return jsonify({'success': False, 'error': 'Phone and message required'})
    
    # Send via Tata API
    token = os.getenv('WHATSAPP_TOKEN')
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'to': phone,
        'type': 'text',
        'text': {'body': message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Tata API response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            # Store message locally
            if phone not in messages_db:
                messages_db[phone] = []
            
            messages_db[phone].append({
                'text': message,
                'type': 'sent',
                'timestamp': datetime.now().isoformat()
            })
            
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': f'Tata API error: {response.text}'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'})

@app.route('/api/chats')
def get_chats():
    chat_list = []
    for phone, contact_info in all_contacts.items():
        messages = messages_db.get(phone, [])
        last_message = messages[-1] if messages else {'text': 'No messages', 'timestamp': ''}
        
        chat_list.append({
            'phone': phone,
            'lastMessage': last_message.get('text', 'No messages'),
            'timestamp': contact_info.get('last_seen', ''),
            'messageCount': len(messages)
        })
    
    stats = {
        'totalMessages': sum(len(msgs) for msgs in messages_db.values()),
        'activeChats': len(all_contacts),
        'aiResponses': 0,
        'successRate': 100
    }
    
    return jsonify({'chats': chat_list, 'stats': stats})

@app.route('/api/messages/<phone>', methods=['GET'])
def get_messages(phone):
    messages = messages_db.get(phone, [])
    return jsonify({'messages': messages})

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print(f"Webhook received: {data}")
    
    # Extract contact info from webhook
    phone = data.get('from')
    if data.get('text'):
        message_text = data['text'].get('body') if isinstance(data['text'], dict) else data['text']
    else:
        message_text = data.get('message')
    
    if phone and message_text:
        print(f"New message from {phone}: {message_text}")
        
        # Store contact
        all_contacts[phone] = {
            'phone': phone,
            'name': 'WhatsApp User',
            'last_seen': datetime.now().isoformat(),
            'total_interactions': all_contacts.get(phone, {}).get('total_interactions', 0) + 1
        }
        
        # Store message
        if phone not in messages_db:
            messages_db[phone] = []
        
        messages_db[phone].append({
            'text': message_text,
            'type': 'received',
            'timestamp': datetime.now().isoformat()
        })
        
        chats_db[phone] = {
            'lastMessage': message_text,
            'timestamp': datetime.now().isoformat()
        }
    
    return jsonify({'status': 'success', 'message': 'received'})

if __name__ == '__main__':
    print("Starting quick fix app...")
    app.run(host='0.0.0.0', port=3000, debug=True)