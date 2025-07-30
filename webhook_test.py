import requests
import json

def test_webhook():
    """Test the webhook endpoint with sample data"""
    url = "http://localhost:3000/webhook"
    
    # Test data in Tata Telecom format
    test_data = {
        "type": "message",
        "from": "+919355421616",
        "text": {
            "body": "Hello, this is a test message!"
        },
        "timestamp": "1640995200"
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed")
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

if __name__ == "__main__":
    print("🧪 Testing webhook endpoint...")
    test_webhook()