import subprocess
import time
import threading
import requests
from pyngrok import ngrok

def start_flask_server():
    """Start Flask server in background"""
    subprocess.Popen(["python", "app.py"], cwd=".")

def main():
    print("🚀 Starting WhatsApp OpenAI Bot with Public URL...")
    
    # Start Flask server
    print("📱 Starting Flask server...")
    start_flask_server()
    time.sleep(3)  # Wait for server to start
    
    try:
        # Start ngrok tunnel
        print("🌐 Creating public tunnel...")
        public_tunnel = ngrok.connect(3000)
        public_url = public_tunnel.public_url
        
        print(f"✅ SUCCESS! Your bot is live at: {public_url}")
        
        # Test the connection
        try:
            response = requests.get(f"{public_url}/")
            if response.status_code == 200:
                print("✅ Server is responding correctly!")
        except:
            pass
        
        print("\n" + "="*70)
        print("📋 COPY THIS CONFIGURATION TO TATA TELECOM PANEL:")
        print("="*70)
        print(f"Name: WhatsApp OpenAI Bot")
        print(f"Type: REST")
        print(f"Method: POST")
        print(f"URL: {public_url}/webhook")
        print(f"Header: Content-Type = application/json")
        print(f"Body Type: application/json")
        print(f"Map entire request body: ✅ CHECK THIS BOX")
        print(f"Response Mapping: Entire Response")
        print("="*70)
        
        print(f"\n🔗 Test your webhook: {public_url}/webhook")
        print(f"📊 Health check: {public_url}/")
        print(f"📞 WhatsApp Number: +919355421616")
        
        print("\n⚠️  IMPORTANT: Keep this terminal open!")
        print("Press Ctrl+C to stop the bot...")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping bot...")
            ngrok.disconnect(public_tunnel.public_url)
            ngrok.kill()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your Flask server is running on port 3000")

if __name__ == "__main__":
    main()