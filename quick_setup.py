from pyngrok import ngrok
import subprocess
import time
import sys

# Configure ngrok with your auth token
ngrok.set_auth_token('30aIC76ukxRypLNs0ZL29BZtKK2_7jnVbHjm1XbPsstUZ3BLE')

# Start Flask server
print("Starting server...")
subprocess.Popen([sys.executable, "app.py"])
time.sleep(2)

# Create tunnel
tunnel = ngrok.connect(3000)
url = tunnel.public_url

print("\n" + "="*60)
print("TATA TELECOM INTEGRATION SETTINGS:")
print("="*60)
print(f"Name: WhatsApp OpenAI Bot")
print(f"Type: REST")
print(f"Method: POST")
print(f"URL: {url}/webhook")
print(f"Header: Content-Type = application/json")
print(f"Body Type: application/json")
print(f"Map entire request body: ✓ ENABLE")
print(f"Response Mapping: Entire Response")
print("="*60)
print(f"Webhook URL: {url}/webhook")
print(f"Test URL: {url}/")
print("="*60)

print("\nYour bot is LIVE! Configure Tata panel with above settings.")
print("Press Ctrl+C to stop...")