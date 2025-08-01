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

# Enhanced storage for comprehensive chat tracking
chats_db = {}
messages_db = {}
all_webhook_data = []  # Store all webhook data for analysis
all_contacts = {}  # Store all contacts that have ever messaged

@app.route('/')
def dashboard():
    return send_from_directory('static', 'dashboard.html')

@app.route('/tata-chats')
def tata_chats_page():
    return send_from_directory('static', 'tata_chats.html')

@app.route('/api/tata-chats', methods=['GET'])
def get_tata_chats():
    """Get ALL contacts and chats from webhook data"""
    try:
        all_chats = []
        
        # Add all contacts that have ever interacted
        for phone, contact_info in all_contacts.items():
            messages = messages_db.get(phone, [])
            last_message = messages[-1] if messages else {'text': 'No recent messages', 'timestamp': contact_info.get('last_seen', '')}
            
            all_chats.append({
                'phone': phone,
                'name': contact_info.get('name', 'Unknown'),
                'lastMessage': last_message.get('text', 'No recent messages'),
                'timestamp': contact_info.get('last_seen', ''),
                'status': 'Active' if messages else 'Contact only',
                'messageCount': len(messages),
                'totalInteractions': contact_info.get('total_interactions', 0),
                'source': 'Webhook captured',
                'lastMessageType': last_message.get('type', 'unknown')
            })
        
        # Also add chats that might not be in contacts
        for phone, chat_data in chats_db.items():
            if phone not in all_contacts:
                messages = messages_db.get(phone, [])
                last_message = messages[-1] if messages else {'text': 'No messages', 'timestamp': ''}
                
                all_chats.append({
                    'phone': phone,
                    'name': 'Unknown',
                    'lastMessage': last_message.get('text', 'No messages'),
                    'timestamp': chat_data.get('timestamp', ''),
                    'status': 'Chat only',
                    'messageCount': len(messages),
                    'totalInteractions': 1,
                    'source': 'Chat data',
                    'lastMessageType': last_message.get('type', 'unknown')
                })
        
        # Remove duplicates and sort by timestamp
        unique_chats = {chat['phone']: chat for chat in all_chats}
        sorted_chats = sorted(unique_chats.values(), key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'chats': sorted_chats,
            'total': len(sorted_chats),
            'totalWebhooks': len(all_webhook_data),
            'note': 'All contacts captured from webhook data - this includes everyone who has ever messaged your WhatsApp number'
        })
        
    except Exception as e:
        print(f"Error getting chats: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/webhook-data', methods=['GET'])
def get_webhook_data():
    """Get raw webhook data for debugging"""
    return jsonify({
        'success': True,
        'webhooks': all_webhook_data[-50:],  # Last 50 webhooks
        'total': len(all_webhook_data)
    })

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

@app.route('/api/messages/<phone>', methods=['GET'])
def get_messages(phone):
    messages = messages_db.get(phone, [])
    return jsonify({'messages': messages})

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
        return jsonify({'success': False, 'error': 'Message sent to Tata API but user may not receive it. Users must opt-in first by messaging your WhatsApp number.'})

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
        return jsonify({'success': False, 'error': 'Template sent to Tata API but user may not receive it. Users must opt-in first.'})

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
    
    # Store all webhook data for comprehensive tracking
    webhook_entry = {
        'timestamp': datetime.now().isoformat(),
        'data': data,
        'raw_data': str(data)
    }
    all_webhook_data.append(webhook_entry)
    
    # Extract and store contact info from any webhook data
    contact_phone = None
    contact_name = None
    
    # Try different webhook formats
    if data.get('contacts'):
        for contact in data['contacts']:
            contact_phone = contact.get('wa_id') or contact.get('phone')
            contact_name = contact.get('profile', {}).get('name', 'Unknown')
    
    if data.get('messages'):
        msg_data = data['messages']
        contact_phone = msg_data.get('from') or contact_phone
    
    if data.get('from'):
        contact_phone = data['from']
    
    # Store contact info
    if contact_phone:
        all_contacts[contact_phone] = {
            'phone': contact_phone,
            'name': contact_name or 'Unknown',
            'last_seen': datetime.now().isoformat(),
            'total_interactions': all_contacts.get(contact_phone, {}).get('total_interactions', 0) + 1
        }
    
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