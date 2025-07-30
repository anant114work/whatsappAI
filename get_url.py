from pyngrok import ngrok
import subprocess
import time

# Set auth token
ngrok.set_auth_token('30aIC76ukxRypLNs0ZL29BZtKK2_7jnVbHjm1XbPsstUZ3BLE')

# Start Flask server in background
subprocess.Popen(["python", "app.py"])
time.sleep(2)

# Create tunnel
tunnel = ngrok.connect(3000)
public_url = tunnel.public_url

print("="*60)
print("TATA TELECOM PANEL CONFIGURATION:")
print("="*60)
print(f"Name: WhatsApp OpenAI Bot")
print(f"Type: REST") 
print(f"Method: POST")
print(f"URL: {public_url}/webhook")
print(f"Content-Type: application/json")
print(f"Body Type: application/json")
print(f"Map entire request body: ✓ CHECK THIS")
print(f"Response Mapping: Entire Response")
print("="*60)
print(f"Public URL: {public_url}")
print(f"Webhook: {public_url}/webhook")
print("="*60)