#!/usr/bin/env python3
"""
Test script for WhatsApp Chat Manager
Simulates incoming messages for testing
"""

import requests
import json
import time

BASE_URL = "http://localhost:3000"

def simulate_incoming_message(phone, message):
    """Simulate an incoming WhatsApp message"""
    webhook_data = {
        "from": phone,
        "text": {"body": message},
        "timestamp": str(int(time.time()))
    }
    
    response = requests.post(f"{BASE_URL}/webhook", json=webhook_data)
    print(f"📨 Sent message from {phone}: {message}")
    print(f"✅ Response: {response.status_code}")

def test_manual_send(phone, message):
    """Test manual message sending"""
    data = {"phone": phone, "message": message}
    response = requests.post(f"{BASE_URL}/api/send", json=data)
    print(f"📤 Manual send to {phone}: {message}")
    print(f"✅ Response: {response.json()}")

def test_ai_toggle(phone):
    """Test AI toggle for a contact"""
    data = {"phone": phone}
    response = requests.post(f"{BASE_URL}/api/toggle-ai", json=data)
    print(f"🤖 AI toggle for {phone}")
    print(f"✅ Response: {response.json()}")

def main():
    print("🧪 Testing WhatsApp Chat Manager")
    print("Make sure the chat manager is running on localhost:3000\n")
    
    test_phone = "+919999999999"
    
    # Test 1: Simulate incoming messages
    print("1. Simulating incoming messages...")
    simulate_incoming_message(test_phone, "Hello, I need help!")
    time.sleep(1)
    simulate_incoming_message(test_phone, "What are your services?")
    time.sleep(1)
    
    # Test 2: Enable AI for this contact
    print("\n2. Enabling AI for contact...")
    test_ai_toggle(test_phone)
    time.sleep(1)
    
    # Test 3: Send another message (should get AI response)
    print("\n3. Sending message with AI enabled...")
    simulate_incoming_message(test_phone, "Tell me about your company")
    time.sleep(2)
    
    # Test 4: Manual message send
    print("\n4. Testing manual message send...")
    test_manual_send(test_phone, "This is a manual reply from admin")
    
    print("\n✅ Tests completed! Check the dashboard at http://localhost:3000")

if __name__ == '__main__':
    main()