import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_send_message():
    """Test sending a message via Tata Telecom API"""
    url = "https://api.smartflo.ai/v1/messages"
    token = os.getenv('WHATSAPP_TOKEN')
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'to': '+919355421616',  # Your WhatsApp number
        'type': 'text',
        'text': {'body': 'Test message from OpenAI Bot! 🤖'}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Message sent successfully!")
        else:
            print("❌ Failed to send message")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Tata Telecom WhatsApp Integration...")
    test_send_message()