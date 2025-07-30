import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_template_message(phone_number):
    """Send template message to initiate conversation"""
    token = os.getenv('WHATSAPP_TOKEN')
    
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'to': phone_number,
        'type': 'template',
        'template': {
            'name': 'welcome_message',
            'language': {'code': 'en'}
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Template message sent to {phone_number}")
            return True
        else:
            print(f"❌ Failed to send template message")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    phone = input("Enter phone number (with country code): ")
    send_template_message(phone)