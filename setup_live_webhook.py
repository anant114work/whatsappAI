#!/usr/bin/env python3
"""
Setup live webhook for WhatsApp Chat Manager
This will help you configure the webhook to receive real messages
"""

import os
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

def start_ngrok():
    """Start ngrok to expose local server"""
    try:
        print("Starting ngrok to expose local server...")
        # Start ngrok in background
        process = subprocess.Popen(['ngrok', 'http', '3000'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for ngrok to start
        import time
        time.sleep(3)
        
        # Get ngrok URL
        response = requests.get('http://localhost:4040/api/tunnels')
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    webhook_url = tunnel['public_url'] + '/webhook'
                    print(f"✅ Webhook URL: {webhook_url}")
                    return webhook_url
        
        print("❌ Could not get ngrok URL")
        return None
        
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        print("Make sure ngrok is installed: https://ngrok.com/download")
        return None

def main():
    print("🔗 WhatsApp Live Webhook Setup")
    print("=" * 40)
    
    # Check if chat manager is running
    try:
        response = requests.get('http://localhost:3000/api/test-connection')
        if response.status_code == 200:
            print("✅ Chat manager is running")
        else:
            print("❌ Chat manager not running. Start it first with: python chat_manager.py")
            return
    except:
        print("❌ Chat manager not running. Start it first with: python chat_manager.py")
        return
    
    # Start ngrok
    webhook_url = start_ngrok()
    if not webhook_url:
        return
    
    print("\n📋 WEBHOOK CONFIGURATION STEPS:")
    print("1. Go to Tata Telecom Business Manager")
    print("2. Navigate to WhatsApp > Settings > Webhook")
    print(f"3. Set Webhook URL: {webhook_url}")
    print(f"4. Set Verify Token: {os.getenv('VERIFY_TOKEN')}")
    print("5. Subscribe to 'messages' events")
    print("\n🧪 TEST YOUR WEBHOOK:")
    print("1. Send a message to your WhatsApp Business number")
    print("2. Check the chat manager at: http://localhost:3000")
    print("3. The message should appear in the contacts list")
    
    print("\n⚠️  IMPORTANT:")
    print("- Keep this script running to maintain the webhook")
    print("- Keep the chat manager running in another terminal")
    print("- Messages will now appear in real-time!")
    
    # Keep ngrok running
    try:
        print("\n🔄 Webhook is active. Press Ctrl+C to stop...")
        while True:
            import time
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n👋 Webhook stopped")

if __name__ == '__main__':
    main()