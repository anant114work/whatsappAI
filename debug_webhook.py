#!/usr/bin/env python3
"""
Debug webhook processing
Test the webhook data extraction functions
"""

import json

# Test data from Tata Telecom format
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

def extract_phone(data):
    # Handle Tata Telecom webhook format from the API docs
    # Format: {"messages": {"from": "919999999999", ...}}
    if data.get('messages'):
        return data.get('messages', {}).get('from')
    # Format: {"contacts": [{"wa_id": "919999999999"}]}
    if data.get('contacts'):
        contacts = data.get('contacts', [])
        if contacts and len(contacts) > 0:
            return contacts[0].get('wa_id')
    # Direct format: {"from": "919999999999"}
    return data.get('from')

def extract_message(data):
    # Handle Tata Telecom webhook format from the API docs
    # Format: {"messages": {"text": {"body": "message"}, "type": "text"}}
    if data.get('messages'):
        msg = data.get('messages', {})
        if msg.get('text') and msg.get('text', {}).get('body'):
            return msg.get('text', {}).get('body')
    # Direct format for testing
    if data.get('text') and data.get('text', {}).get('body'):
        return data.get('text', {}).get('body')
    return None

def main():
    print("Webhook Data Extraction Debug")
    print("=" * 30)
    
    print(f"Test data: {json.dumps(test_data, indent=2)}")
    print()
    
    phone = extract_phone(test_data)
    message = extract_message(test_data)
    
    print(f"Extracted phone: {phone}")
    print(f"Extracted message: {message}")
    
    if phone and message:
        print("SUCCESS: Both phone and message extracted correctly")
    else:
        print("ERROR: Failed to extract phone or message")
        
        # Debug each part
        print("\nDebugging:")
        print(f"data.get('messages'): {test_data.get('messages')}")
        print(f"data.get('contacts'): {test_data.get('contacts')}")
        
        if test_data.get('messages'):
            msg = test_data.get('messages', {})
            print(f"messages.get('from'): {msg.get('from')}")
            print(f"messages.get('text'): {msg.get('text')}")
            if msg.get('text'):
                print(f"text.get('body'): {msg.get('text', {}).get('body')}")

if __name__ == '__main__':
    main()