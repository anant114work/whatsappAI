import requests

def test_local_server():
    try:
        # Test if server is running
        response = requests.get("http://localhost:3000/")
        print(f"Server status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Test the template endpoint
        response = requests.post("http://localhost:3000/api/send-template", 
                               json={"phone": "+918882443789"})
        print(f"Template status: {response.status_code}")
        print(f"Template response: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on localhost:3000")
        print("Run: python app.py")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_local_server()