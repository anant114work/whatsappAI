import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_template():
    token = os.getenv('WHATSAPP_TOKEN')
    
    url = "https://wb.omni.tatatelebusiness.com/templates"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    template_data = {
        "name": "ai_response_template",
        "language": "en",
        "category": "UTILITY",
        "components": [
            {
                "type": "BODY",
                "text": "{{1}}"
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=template_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Template created successfully!")
            return response.json().get('id')
        else:
            print("❌ Failed to create template")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    template_id = create_template()
    if template_id:
        print(f"Template ID: {template_id}")