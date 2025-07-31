#!/usr/bin/env python3
"""
Setup real webhook to receive customer messages
This will expose your local server and help configure the webhook
"""

import os
import requests
import subprocess
import time
import json
from dotenv import load_dotenv

load_dotenv()

def check_ngrok():
    """Check if ngrok is running and get the URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if response.status_code == 200:
            tunnels = response.json().get('tunnels', [])
            for tunnel in tunnels:
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
    except:
        pass
    return None

def start_ngrok():
    """Start ngrok to expose local server"""
    print("Starting ngrok...")
    try:
        # Start ngrok in background
        subprocess.Popen(['ngrok', 'http', '3000'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait for ngrok to start
        for i in range(10):
            time.sleep(2)
            url = check_ngrok()
            if url:
                return url
        
        print("Failed to get ngrok URL")
        return None
        
    except FileNotFoundError:
        print("ERROR: ngrok not found!")
        print("Please install ngrok from: https://ngrok.com/download")
        return None
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None

def test_webhook_endpoint(webhook_url):
    """Test if the webhook endpoint is accessible"""
    try:
        # Test GET request for webhook verification
        test_url = f"{webhook_url}?hub.mode=subscribe&hub.verify_token={os.getenv('VERIFY_TOKEN')}&hub.challenge=test123"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200 and response.text == 'test123':
            print("✅ Webhook endpoint is working correctly")
            return True
        else:
            print(f"❌ Webhook test failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test error: {e}")
        return False

def main():
    print("🔗 WhatsApp Real Webhook Setup")
    print("=" * 40)
    
    # Check if chat manager is running
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code != 200:
            print("❌ Chat manager not running!")
            print("Start it first: python chat_manager.py")
            return
    except:
        print("❌ Chat manager not running!")
        print("Start it first: python chat_manager.py")
        return
    
    print("✅ Chat manager is running")
    
    # Check if ngrok is already running
    webhook_url = check_ngrok()
    
    if not webhook_url:
        print("Starting ngrok to expose your server...")
        webhook_url = start_ngrok()
    
    if not webhook_url:
        print("❌ Failed to start ngrok")
        return
    
    full_webhook_url = webhook_url + '/webhook'
    print(f"✅ Webhook URL: {full_webhook_url}")
    
    # Test webhook endpoint
    if not test_webhook_endpoint(full_webhook_url):
        return
    
    print("\n📋 WEBHOOK CONFIGURATION STEPS:")
    print("1. Go to Meta Business Manager (business.facebook.com)")
    print("2. Select your WhatsApp Business Account")
    print("3. Go to WhatsApp > Configuration")
    print("4. In the Webhook section:")
    print(f"   - Callback URL: {full_webhook_url}")
    print(f"   - Verify Token: {os.getenv('VERIFY_TOKEN')}")
    print("5. Click 'Verify and Save'")
    print("6. Subscribe to 'messages' webhook field")
    
    print("\n🧪 TEST YOUR SETUP:")
    print("1. Send a message to your WhatsApp Business number")
    print("2. Check the chat manager dashboard: http://localhost:3000")
    print("3. The customer message should appear immediately")
    
    print("\n📱 Your WhatsApp Business Number:")
    print(f"   Phone: +{os.getenv('WHATSAPP_PHONE_NUMBER_ID', 'Not configured')}")
    
    print("\n⚠️  IMPORTANT:")
    print("- Keep this script running to maintain the webhook")
    print("- Keep the chat manager running in another terminal")
    print("- Customer messages will now appear in real-time!")
    
    # Keep running
    try:
        print(f"\n🔄 Webhook active at: {full_webhook_url}")
        print("Press Ctrl+C to stop...")
        while True:
            time.sleep(30)
            # Check if ngrok is still running
            if not check_ngrok():
                print("❌ ngrok stopped, restarting...")
                webhook_url = start_ngrok()
                if webhook_url:
                    print(f"✅ New webhook URL: {webhook_url}/webhook")
                else:
                    print("❌ Failed to restart ngrok")
                    break
    except KeyboardInterrupt:
        print("\n👋 Webhook stopped")

if __name__ == '__main__':
    main()