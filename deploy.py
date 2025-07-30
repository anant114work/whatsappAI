import subprocess
import time
import requests

def deploy():
    print("Starting server...")
    
    # Start server
    process = subprocess.Popen(['python', 'production_server.py'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    time.sleep(3)  # Wait for server to start
    
    try:
        # Test local server
        response = requests.get('http://localhost:3000/')
        if response.status_code == 200:
            print("✅ Server running on http://localhost:3000")
            
            # Start ngrok
            print("Starting ngrok tunnel...")
            ngrok_process = subprocess.Popen(['ngrok', 'http', '3000'], 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE)
            
            time.sleep(5)  # Wait for ngrok to start
            
            # Get ngrok URL
            try:
                tunnels = requests.get('http://localhost:4040/api/tunnels').json()
                public_url = tunnels['tunnels'][0]['public_url']
                
                print(f"🌐 Public URL: {public_url}")
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
                print("\nSample Body:")
                print('{"from": "{{phone}}", "text": {"body": "{{message}}"}}')
                print("\nResponse Mapping: Entire Response")
                print("="*60)
                
                input("Press Enter to stop servers...")
                
            except:
                print("❌ Could not get ngrok URL. Make sure ngrok is installed.")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        process.terminate()
        try:
            ngrok_process.terminate()
        except:
            pass

if __name__ == "__main__":
    deploy()