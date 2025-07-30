from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

# OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/', methods=['GET'])
def health_check():
    return app.send_static_file('index.html')

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'running',
        'service': 'WhatsApp OpenAI Bot',
        'phone': '+919355421616',
        'webhook': '/webhook'
    })

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    print(f"Webhook verification: mode={mode}, token={token}")
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print('✅ Webhook verified successfully')
        return challenge
    
    print('❌ Webhook verification failed')
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print(f"Received webhook data: {data}")
    
    # Handle Tata Telecom Smartflo webhook format
    if data.get('type') == 'message':
        handle_message(data)
    elif data.get('messages'):  # Alternative format
        for message in data.get('messages', []):
            handle_message(message)
    elif data.get('object') == 'whatsapp_business_account':  # Meta format fallback
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'messages':
                    messages = change.get('value', {}).get('messages', [])
                    for message in messages:
                        handle_message(message)
    
    return jsonify({'status': 'success', 'message': 'received'})

def handle_message(message):
    # Handle different message formats from Tata Telecom
    from_number = None
    text = None
    
    # Format 1: Direct message object
    if message.get('from'):
        from_number = message.get('from')
        if message.get('text'):
            text = message.get('text', {}).get('body') or message.get('text')
    
    # Format 2: Nested structure
    elif message.get('sender'):
        from_number = message.get('sender')
        text = message.get('message', {}).get('text') or message.get('body')
    
    # Format 3: Alternative structure
    elif message.get('phone'):
        from_number = message.get('phone')
        text = message.get('content') or message.get('message')
    
    if from_number and text:
        print(f"Received from {from_number}: {text}")
        
        try:
            # Get AI response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful WhatsApp assistant. Keep responses brief and friendly."},
                    {"role": "user", "content": text}
                ],
                max_tokens=150
            )
            
            ai_response = response.choices[0].message.content
            send_message(from_number, ai_response)
            
        except Exception as e:
            print(f"Error processing message: {e}")
            send_message(from_number, "Sorry, I encountered an error. Please try again.")
    else:
        print(f"Could not extract message data: {message}")

def send_message(to, message):
    # Try multiple Tata Telecom API endpoints
    endpoints = [
        "https://api.smartflo.ai/v1/messages",
        "https://api.smartflo.ai/messages",
        "https://smartflo.ai/api/v1/messages"
    ]
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Try different payload formats
    payloads = [
        {
            'to': to,
            'type': 'text',
            'text': {'body': message}
        },
        {
            'phone': to,
            'message': message,
            'type': 'text'
        },
        {
            'recipient': to,
            'content': message,
            'message_type': 'text'
        }
    ]
    
    for endpoint in endpoints:
        for payload in payloads:
            try:
                response = requests.post(endpoint, headers=headers, json=payload)
                if response.status_code in [200, 201]:
                    print(f"Message sent successfully via {endpoint}")
                    return True
                else:
                    print(f"Failed with {endpoint}: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
    
    print("Failed to send message with all endpoints")
    return False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)