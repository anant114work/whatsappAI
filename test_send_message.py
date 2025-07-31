#!/usr/bin/env python3
"""
Test WhatsApp message sending directly
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_send_message():
    """Test sending a WhatsApp message using Tata Telecom API"""
    
    url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/messages"
    token = os.getenv('WHATSAPP_TOKEN')
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    payload = {
        "to": "+919999999999",  # Test number
        "type": "text",
        "source": "external",
        "text": {
            "body": "Test message from API"
        }
    }
    
    print("Testing WhatsApp Message Send")
    print("=" * 30)
    print(f"URL: {url}")
    print(f"Token: {token[:20]}..." if token else "No token found")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"SUCCESS: Message ID = {data.get('id', 'No ID')}")
            except:
                print("SUCCESS: Message sent (non-JSON response)")
        else:
            print("FAILED: Check the error details above")
            
            # Common error explanations
            if response.status_code == 401:
                print("ERROR: Authentication failed - check WHATSAPP_TOKEN in .env")
            elif response.status_code == 400:
                print("ERROR: Bad request - check message format")
            elif response.status_code == 424:
                print("ERROR: WhatsApp API error - phone number may not have calling permissions")
                
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    test_send_message()