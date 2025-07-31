#!/usr/bin/env python3
"""
Check current webhook status and configuration
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_local_webhook():
    """Check if local webhook is responding"""
    try:
        # Test webhook verification
        url = f"http://localhost:3000/webhook?hub.mode=subscribe&hub.verify_token={os.getenv('VERIFY_TOKEN')}&hub.challenge=test123"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200 and response.text == 'test123':
            print("Local webhook is working")
            return True
        else:
            print(f"Local webhook failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Local webhook error: {e}")
        return False

def check_chat_manager():
    """Check if chat manager is running"""
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("Chat manager is running")
            return True
        else:
            print("Chat manager not responding")
            return False
    except Exception as e:
        print(f"Chat manager error: {e}")
        return False

def check_api_connection():
    """Check WhatsApp API connection"""
    try:
        url = "https://wb.omni.tatatelebusiness.com/whatsapp-cloud/settings"
        headers = {
            'Authorization': os.getenv('WHATSAPP_TOKEN'),
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("WhatsApp API connection working")
            return True
        else:
            print(f"WhatsApp API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"WhatsApp API error: {e}")
        return False

def main():
    print("WhatsApp Webhook Status Check")
    print("=" * 35)
    
    print("\n1. Checking Chat Manager...")
    chat_ok = check_chat_manager()
    
    print("\n2. Checking Local Webhook...")
    webhook_ok = check_local_webhook()
    
    print("\n3. Checking WhatsApp API...")
    api_ok = check_api_connection()
    
    print("\nSUMMARY:")
    print(f"Chat Manager: {'OK' if chat_ok else 'FAIL'}")
    print(f"Local Webhook: {'OK' if webhook_ok else 'FAIL'}")
    print(f"WhatsApp API: {'OK' if api_ok else 'FAIL'}")
    
    if all([chat_ok, webhook_ok, api_ok]):
        print("\nAll systems working!")
        print("If you're not receiving customer messages, you need to:")
        print("1. Expose your server with ngrok: python setup_real_webhook.py")
        print("2. Configure the webhook URL in Meta Business Manager")
    else:
        print("\nIssues found:")
        if not chat_ok:
            print("- Start chat manager: python chat_manager.py")
        if not webhook_ok:
            print("- Check webhook configuration")
        if not api_ok:
            print("- Check WHATSAPP_TOKEN in .env file")

if __name__ == '__main__':
    main()