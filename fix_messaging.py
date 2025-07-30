import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_send_to_new_number():
    """Test sending message to a new number"""
    token = os.getenv('WHATSAPP_TOKEN')
    phone = "+918882443789"
    
    # First try template message
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Try template first
    template_payload = {
        'to': phone,
        'type': 'template',
        'template': {
            'name': 'hello_world',
            'language': {'code': 'en_US'}
        }
    }
    
    print("Trying template message...")
    response = requests.post(url, headers=headers, json=template_payload)
    print(f"Template Status: {response.status_code}")
    print(f"Template Response: {response.text}")
    
    if response.status_code != 200:
        # Try session message
        session_payload = {
            'to': phone,
            'type': 'text',
            'text': {'body': 'Hello! This is a test message from AI Bot 🤖'}
        }
        
        print("\nTrying session message...")
        response = requests.post(url, headers=headers, json=session_payload)
        print(f"Session Status: {response.status_code}")
        print(f"Session Response: {response.text}")

if __name__ == "__main__":
    test_send_to_new_number()