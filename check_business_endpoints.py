import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_business_endpoints():
    token = os.getenv('WHATSAPP_TOKEN')
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Since /business/profile works, try related business endpoints
    business_endpoints = [
        'https://wb.omni.tatatelebusiness.com/business/profile',
        'https://wb.omni.tatatelebusiness.com/business/contacts',
        'https://wb.omni.tatatelebusiness.com/business/conversations',
        'https://wb.omni.tatatelebusiness.com/business/messages',
        'https://wb.omni.tatatelebusiness.com/business/customers',
        'https://wb.omni.tatatelebusiness.com/business/chats',
        'https://wb.omni.tatatelebusiness.com/business/users',
        
        # Try analytics endpoints (might have contact data)
        'https://wb.omni.tatatelebusiness.com/analytics/contacts',
        'https://wb.omni.tatatelebusiness.com/analytics/conversations',
        
        # Try settings endpoints
        'https://wb.omni.tatatelebusiness.com/settings/contacts',
        'https://wb.omni.tatatelebusiness.com/whatsapp-cloud/settings',
        
        # Try phone number specific endpoints
        'https://wb.omni.tatatelebusiness.com/whatsapp-cloud/phone_numbers',
        'https://wb.omni.tatatelebusiness.com/phone_numbers'
    ]
    
    working_endpoints = []
    
    for endpoint in business_endpoints:
        try:
            print(f"Testing: {endpoint}")
            response = requests.get(endpoint, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS: {response.status_code}")
                print(f"Data: {str(data)[:500]}...")
                working_endpoints.append((endpoint, data))
            else:
                print(f"❌ {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        print()
    
    return working_endpoints

if __name__ == "__main__":
    working = check_business_endpoints()
    print(f"\n🎉 Found {len(working)} working endpoints:")
    for endpoint, data in working:
        print(f"- {endpoint}")