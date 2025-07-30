import requests
import os
from dotenv import load_dotenv

load_dotenv()

def setup_tata_webhook():
    """Setup webhook with Tata Telecom Smartflo"""
    
    # Your webhook URL (use ngrok for testing)
    webhook_url = input("Enter your webhook URL (e.g., https://your-ngrok-url.ngrok.io/webhook): ")
    
    if not webhook_url:
        webhook_url = "https://your-domain.com/webhook"
        print(f"Using default: {webhook_url}")
    
    token = os.getenv('WHATSAPP_TOKEN')
    
    # Tata Telecom webhook setup endpoint (this may vary)
    setup_endpoints = [
        "https://api.smartflo.ai/v1/webhook",
        "https://api.smartflo.ai/webhook/setup",
        "https://smartflo.ai/api/v1/webhook"
    ]
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    webhook_config = {
        'url': webhook_url,
        'events': ['message', 'delivery', 'read'],
        'verify_token': os.getenv('VERIFY_TOKEN')
    }
    
    print(f"Setting up webhook: {webhook_url}")
    print(f"Token: {token[:20]}...")
    
    for endpoint in setup_endpoints:
        try:
            response = requests.post(endpoint, headers=headers, json=webhook_config)
            print(f"\\nTrying {endpoint}:")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code in [200, 201]:
                print("✅ Webhook setup successful!")
                return True
                
        except Exception as e:
            print(f"❌ Error with {endpoint}: {e}")
            continue
    
    print("\\n📝 Manual Setup Instructions:")
    print("1. Login to your Tata Telecom Smartflo dashboard")
    print("2. Go to Settings > Webhooks")
    print(f"3. Add webhook URL: {webhook_url}")
    print(f"4. Set verify token: {os.getenv('VERIFY_TOKEN')}")
    print("5. Enable message events")
    
    return False

if __name__ == "__main__":
    print("🔧 Setting up Tata Telecom webhook...")
    setup_tata_webhook()