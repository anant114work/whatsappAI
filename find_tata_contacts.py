import requests
import os
from dotenv import load_dotenv

load_dotenv()

def find_tata_contacts():
    token = os.getenv('WHATSAPP_TOKEN')
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Based on Tata's API docs, try these endpoints
    endpoints = [
        # Customer/Contact endpoints
        'https://wb.omni.tatatelebusiness.com/business/contacts',
        'https://wb.omni.tatatelebusiness.com/customers/list',
        'https://wb.omni.tatatelebusiness.com/api/customers',
        
        # Message history endpoints  
        'https://wb.omni.tatatelebusiness.com/messages/history',
        'https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages/history',
        
        # Business/Account endpoints
        'https://wb.omni.tatatelebusiness.com/business/profile',
        'https://wb.omni.tatatelebusiness.com/account/contacts',
        
        # Try with different paths
        'https://wb.omni.tatatelebusiness.com/v1/contacts',
        'https://wb.omni.tatatelebusiness.com/v1/customers',
        'https://wb.omni.tatatelebusiness.com/v1/conversations'
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\nTrying: {endpoint}")
            response = requests.get(endpoint, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"SUCCESS! Found data: {str(data)[:300]}...")
                return endpoint, data
            elif response.status_code == 401:
                print("Unauthorized - check token")
            elif response.status_code == 404:
                print("Not found")
            else:
                print(f"Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nNo working endpoints found. Tata may not expose chat history via API.")
    return None, None

if __name__ == "__main__":
    endpoint, data = find_tata_contacts()
    if endpoint:
        print(f"\nWorking endpoint: {endpoint}")
        print("Use this in your Flask app!")