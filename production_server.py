from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'active', 'service': 'WhatsApp AI Bot'})

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    phone = data.get('from') or data.get('phone')
    message = data.get('text', {}).get('body') or data.get('message')
    
    if phone and message:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Keep responses under 100 words."},
                    {"role": "user", "content": message}
                ],
                max_tokens=100
            )
            
            ai_reply = response.choices[0].message.content
            
            # Send back to Tata API
            requests.post('https://api.smartflo.ai/v1/messages', 
                headers={'Authorization': f'Bearer {WHATSAPP_TOKEN}', 'Content-Type': 'application/json'},
                json={'to': phone, 'type': 'text', 'text': {'body': ai_reply}})
            
        except Exception as e:
            print(f"Error: {e}")
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)