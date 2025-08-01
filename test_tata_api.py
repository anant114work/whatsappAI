import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_tata_endpoints():
    token = os.getenv('WHATSAPP_TOKEN')
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test different Tata API endpoints based on their documentation
    endpoints = [
        'https://wb.omni.tatatelebusiness.com/contacts',
        'https://wb.omni.tatatelebusiness.com/customers',
        'https://wb.omni.tatatelebusiness.com/users',
        'https://wb.omni.tatatelebusiness.com/conversations',
        'https://wb.omni.tatatelebusiness.com/chats',
        'https://wb.omni.tatatelebusiness.com/messages',
        'https://wb.omni.tatatelebusiness.com/whatsapp-cloud/contacts',
        'https://wb.omni.tatatelebusiness.com/api/contacts',
        'https://wb.omni.tatatelebusiness.com/api/customers'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers)
            print(f"\n{endpoint}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.text[:300]}...")
            else:
                print(f"Error: {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_tata_endpoints()