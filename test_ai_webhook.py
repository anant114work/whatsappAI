import requests
import json

def test_ai_webhook():
    """Test the AI webhook with a sample message"""
    url = "http://localhost:3000/webhook"
    
    # Test message from Tata format
    test_data = {
        "from": "+918882443789",
        "text": {
            "body": "Hello, how are you?"
        },
        "timestamp": "1640995200"
    }
    
    try:
        print("Sending test message to webhook...")
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook received message successfully!")
            print("Check your terminal for AI processing logs")
        else:
            print("❌ Webhook test failed")
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

if __name__ == "__main__":
    test_ai_webhook()