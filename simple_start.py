import subprocess
import time
import requests
from pyngrok import ngrok

def main():
    print("Starting WhatsApp OpenAI Bot...")
    
    # Start Flask server
    subprocess.Popen(["python", "app.py"], cwd=".")
    time.sleep(3)
    
    try:
        # Start ngrok tunnel
        public_tunnel = ngrok.connect(3000)
        public_url = public_tunnel.public_url
        
        print(f"SUCCESS! Bot is live at: {public_url}")
        
        print("\n" + "="*60)
        print("TATA TELECOM PANEL CONFIGURATION:")
        print("="*60)
        print(f"Name: WhatsApp OpenAI Bot")
        print(f"Type: REST")
        print(f"Method: POST")
        print(f"URL: {public_url}/webhook")
        print(f"Header: Content-Type = application/json")
        print(f"Body Type: application/json")
        print(f"Map entire request body: CHECK THIS BOX")
        print(f"Response Mapping: Entire Response")
        print("="*60)
        
        print(f"\nWebhook URL: {public_url}/webhook")
        print(f"Health check: {public_url}/")
        print(f"WhatsApp: +919355421616")
        
        print("\nKeep this terminal open! Press Ctrl+C to stop...")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
        ngrok.disconnect(public_tunnel.public_url)
        ngrok.kill()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()