import requests

def test_import():
    contact = {
        "phone": "+919876543210",
        "name": "Test Customer",
        "lastMessage": "Test message from Tata panel"
    }
    
    try:
        response = requests.post('http://localhost:3000/api/import-contact', json=contact)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_import()