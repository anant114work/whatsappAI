"""
To get REAL contacts from your Tata panel:

1. Go to your Tata Telecom dashboard
2. Look for "Customers" or "Contacts" section
3. Export/download your contact list (usually CSV/Excel)
4. Replace the contacts below with your actual data

OR

Ask someone to send a message to +919355421616 
The webhook will automatically capture them as real contacts.
"""

# Replace these with your ACTUAL Tata panel contacts
REAL_CONTACTS = [
    # Copy from your Tata panel export
    {"phone": "+919876543210", "name": "Actual Customer 1", "lastMessage": "Real message from panel"},
    {"phone": "+918765432109", "name": "Actual Customer 2", "lastMessage": "Real conversation"},
    # Add more real contacts here...
]

import requests

def import_real_contacts():
    for contact in REAL_CONTACTS:
        try:
            response = requests.post('http://localhost:3000/api/import-contact', json=contact)
            print(f"Imported {contact['name']}: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Replace REAL_CONTACTS with your actual Tata panel data")
    print("Then run this script to import them")
    # import_real_contacts()  # Uncomment when you add real data