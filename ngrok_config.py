from pyngrok import ngrok
import subprocess
import time
import sys

def setup_ngrok():
    try:
        # Set auth token
        ngrok.set_auth_token('30aIC76ukxRypLNs0ZL29BZtKK2_7jnVbHjm1XbPsstUZ3BLE')
        
        # Start Flask server
        print("Starting Flask server...")
        subprocess.Popen([sys.executable, "app.py"])
        time.sleep(3)
        
        # Create ngrok tunnel
        print("Creating ngrok tunnel...")
        tunnel = ngrok.connect(3000)
        public_url = tunnel.public_url
        
        print("\n" + "="*70)
        print("COPY THESE SETTINGS TO TATA TELECOM PANEL:")
        print("="*70)
        print(f"Name: WhatsApp OpenAI Bot")
        print(f"Access ID: (leave blank)")
        print(f"Type: REST")
        print(f"Method: POST")
        print(f"URL: {public_url}/webhook")
        print("")
        print("HEADERS:")
        print("Content-Type: application/json")
        print("")
        print("BODY SETTINGS:")
        print("Select body type: application/json")
        print("Map the entire request body: ✓ CHECK THIS BOX")
        print("")
        print("RESPONSE MAPPING:")
        print("Success Response Mapping: Entire Response")
        print("Error Response Mapping: (leave blank)")
        print("="*70)
        print(f"Your webhook URL: {public_url}/webhook")
        print(f"Test URL: {public_url}/")
        print("="*70)
        
        return public_url
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    url = setup_ngrok()
    if url:
        print(f"\nBot is running at: {url}")
        print("Keep this terminal open!")
        input("Press Enter to stop...")
        ngrok.kill()