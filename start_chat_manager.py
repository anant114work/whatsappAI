#!/usr/bin/env python3
"""
WhatsApp Chat Manager Startup Script
Run this to start the chat management interface
"""

import os
import sys
from chat_manager import app

def main():
    print("Starting WhatsApp Chat Manager...")
    print("Dashboard: http://localhost:3000")
    print("Webhook: http://localhost:3000/webhook")
    print("Features: Manual replies, AI toggle, Real-time monitoring")
    print("=" * 50)
    
    try:
        port = int(os.environ.get('PORT', 3000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\nChat Manager stopped")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()