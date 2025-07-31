#!/usr/bin/env python3
"""
Complete WhatsApp Chat Manager Startup
This starts everything needed to receive customer messages
"""

import subprocess
import time
import requests
import os

def main():
    print("Starting Complete WhatsApp Chat Manager System")
    print("=" * 50)
    
    print("Step 1: Starting Chat Manager...")
    print("Run this command in a separate terminal:")
    print("python chat_manager.py")
    print()
    
    print("Step 2: After chat manager is running, expose it with ngrok:")
    print("Run this command in another terminal:")
    print("ngrok http 3000")
    print()
    
    print("Step 3: Configure webhook in Meta Business Manager:")
    print("1. Go to business.facebook.com")
    print("2. Select your WhatsApp Business Account")
    print("3. Go to WhatsApp > Configuration")
    print("4. Set Webhook URL: https://your-ngrok-url.com/webhook")
    print(f"5. Set Verify Token: {os.getenv('VERIFY_TOKEN', 'tata_webhook_verify_2024')}")
    print("6. Subscribe to 'messages' events")
    print()
    
    print("Step 4: Test by sending a message to your WhatsApp Business number")
    print("The message should appear at: http://localhost:3000")
    print()
    
    print("IMPORTANT:")
    print("- Keep both terminals running (chat manager + ngrok)")
    print("- Customer messages will appear in real-time")
    print("- You can reply manually or enable AI per contact")

if __name__ == '__main__':
    main()