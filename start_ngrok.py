import subprocess
import time
import requests
import json
from pyngrok import ngrok

def start_tunnel():
    try:
        # Start ngrok tunnel
        public_tunnel = ngrok.connect(3000)
        public_url = public_tunnel.public_url
        
        print(f"✅ Ngrok tunnel started!")
        print(f"🌐 Public URL: {public_url}")
        print(f"📡 Webhook URL: {public_url}/webhook")
        
        # Test the tunnel
        try:
            response = requests.get(f"{public_url}/")
            if response.status_code == 200:
                print("✅ Tunnel is working!")
            else:
                print("❌ Tunnel test failed")
        except:
            print("⚠️ Could not test tunnel")
        
        print("\n" + "="*60)
        print("TATA TELECOM PANEL CONFIGURATION:")
        print("="*60)
        print(f"Name: WhatsApp OpenAI Bot")
        print(f"Type: REST")
        print(f"Method: POST")
        print(f"URL: {public_url}/webhook")
        print(f"Content-Type: application/json")
        print(f"Body Type: application/json")
        print(f"Map entire request body: ✅ CHECKED")
        print("="*60)
        
        print("\nPress Ctrl+C to stop the tunnel...")
        
        # Keep tunnel alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping tunnel...")
            ngrok.disconnect(public_tunnel.public_url)
            ngrok.kill()
            
    except Exception as e:
        print(f"❌ Error starting tunnel: {e}")
        print("Installing pyngrok...")
        subprocess.run(["pip", "install", "pyngrok"])
        print("Please run this script again.")

if __name__ == "__main__":
    start_tunnel()