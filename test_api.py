import requests

def test_api():
    url = "https://whatsappai-x52i.onrender.com/api/send-template"
    
    data = {
        "phone": "+918882443789"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()