#!/usr/bin/env python3
"""
Setup webhook for WhatsApp Chat Manager
Configure your webhook URL with Tata Telecom
"""

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("WhatsApp Chat Manager Webhook Setup")
    print("=" * 40)
    
    # Get current configuration
    token = os.getenv('WHATSAPP_TOKEN')
    phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    verify_token = os.getenv('VERIFY_TOKEN')
    
    print(f"Phone Number ID: {phone_id}")
    print(f"Verify Token: {verify_token}")
    print()
    
    print("WEBHOOK CONFIGURATION STEPS:")
    print("1. Start the chat manager: python chat_manager.py")
    print("2. Expose your local server using ngrok or similar:")
    print("   ngrok http 3000")
    print()
    print("3. In Tata Telecom Business Manager:")
    print("   - Go to WhatsApp > Configuration")
    print("   - Set Webhook URL: https://your-ngrok-url.com/webhook")
    print(f"   - Set Verify Token: {verify_token}")
    print("   - Subscribe to 'messages' events")
    print()
    print("4. Test the webhook:")
    print("   - Send a message to your WhatsApp Business number")
    print("   - Check the chat manager dashboard at http://localhost:3000")
    print()
    print("IMPORTANT:")
    print("- Make sure your server is running before configuring webhook")
    print("- Use HTTPS URL for webhook (ngrok provides this)")
    print("- Keep the chat manager running to receive messages")

if __name__ == '__main__':
    main()