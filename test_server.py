import requests
import json

def test_server():
    try:
        # Test if server is running
        response = requests.get('http://localhost:3000/', timeout=5)
        print(f"Server status: {response.status_code}")
        
        # Test the send endpoint
        data = {
            "phone": "+918882443789",
            "message": "Test message"
        }
        
        response = requests.post(
            'http://localhost:3000/api/send',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Send API status: {response.status_code}")
        print(f"Send API response: {response.text}")
        
        if response.text:
            try:
                result = response.json()
                print(f"JSON result: {result}")
            except:
                print("Response is not JSON")
        else:
            print("Empty response from server")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Server not running. Start with: python chat_manager.py")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    test_server()