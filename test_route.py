import requests

def test_route():
    try:
        response = requests.post("http://localhost:3000/api/send-template", 
                               json={"phone": "+918882443789"})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Headers: {response.headers}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_route()