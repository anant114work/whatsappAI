#!/usr/bin/env python3
"""
Test webhook message reception
Send a test message to verify the chat manager receives it properly
"""

import requests
import json

def send_test_webhook():
    """Send a test webhook message to the chat manager"""
    
    # Test message in Tata Telecom format based on API docs
    test_data = {
        "contacts": [
            {
                "profile": {
                    "name": "Test User"
                },
                "wa_id": "919999999999"
            }
        ],
        "messages": {
            "from": "919999999999",
            "id": "test_message_123",
            "timestamp": "1744109205",
            "text": {
                "body": "Hello! This is a test message from webhook."
            },
            "type": "text"
        },
        "businessPhoneNumber": "+919355421616"
    }
    
    try:
        print("Sending test webhook message...")
        print(f"Test data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            'http://localhost:3000/webhook',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            print("Test message sent successfully!")
            print("Check the chat manager dashboard at: http://localhost:3000")
            print("You should see the test contact with the message")
        else:
            print("Test message failed")
            
    except Exception as e:
        print(f"Error sending test message: {e}")
        print("Make sure the chat manager is running on localhost:3000")

def main():
    print("WhatsApp Webhook Message Test")
    print("=" * 35)
    
    # Check if chat manager is running
    try:
        response = requests.get('http://localhost:3000/')
        if response.status_code == 200:
            print("Chat manager is running")
            send_test_webhook()
        else:
            print("Chat manager not responding")
    except:
        print("Chat manager not running")
        print("Start it first with: python chat_manager.py")

if __name__ == '__main__':
    main()