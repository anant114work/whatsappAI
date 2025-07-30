import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_opt_in_template():
    """Create a template for opt-in messages"""
    token = os.getenv('WHATSAPP_TOKEN')
    
    url = "https://wb.omni.tatatelebusiness.com/templates"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    template_data = {
        "name": "welcome_message",
        "language": "en",
        "category": "UTILITY",
        "components": [
            {
                "type": "BODY",
                "text": "Hello! Welcome to our AI assistant. Reply with any message to start chatting with our AI bot. 🤖"
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=template_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Opt-in template created successfully!")
            return True
        else:
            print("❌ Failed to create template")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    create_opt_in_template()