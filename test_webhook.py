import requests
import json

# Test the webhook with sample data
url = "https://whatsappai-x52i.onrender.com/webhook"

test_data = {
    "from": "+919355421616",
    "text": {
        "body": "Hi"
    }
}

response = requests.post(url, json=test_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")