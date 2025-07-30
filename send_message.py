import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_message(to_number, message):
    token = os.getenv('WHATSAPP_TOKEN')
    phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    
    # Try Tata Telecom API endpoints
    endpoints = [
        f"https://graph.facebook.com/v18.0/{phone_id}/messages",
        "https://api.smartflo.ai/v1/messages",
        "https://api.smartflo.ai/send"
    ]
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payloads = [
        {
            'messaging_product': 'whatsapp',
            'to': to_number,
            'text': {'body': message}
        },
        {
            'to': to_number,
            'type': 'text',
            'text': {'body': message}
        },
        {
            'phone': to_number,
            'message': message
        }
    ]
    
    for endpoint in endpoints:
        for payload in payloads:
            try:
                response = requests.post(endpoint, headers=headers, json=payload)
                print(f"Trying {endpoint}: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code in [200, 201]:
                    print(f"✅ Message sent successfully!")
                    return True
                    
            except Exception as e:
                print(f"Error: {e}")
                continue
    
    print("❌ Failed to send message")
    return False

if __name__ == "__main__":
    # Send test message
    to = input("Enter recipient number (with country code): ")
    msg = input("Enter message: ")
    
    send_whatsapp_message(to, msg)