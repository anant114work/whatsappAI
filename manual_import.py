"""
Manual import of existing Tata panel contacts
Since Tata doesn't provide API for historical chats, manually add your contacts here
"""

# Add your actual Tata panel contacts here
EXISTING_CONTACTS = [
    {
        "phone": "+919876543210",
        "name": "Customer 1",
        "lastMessage": "Previous conversation from Tata panel",
        "status": "Existing customer"
    },
    {
        "phone": "+918765432109", 
        "name": "Customer 2",
        "lastMessage": "Old chat from panel",
        "status": "Previous inquiry"
    },
    # Add more contacts from your Tata panel here
]

def import_contacts():
    import requests
    
    # Import each contact via API
    for contact in EXISTING_CONTACTS:
        try:
            # Add to local system
            response = requests.post('http://localhost:3000/api/import-contact', 
                                   json=contact)
            print(f"Imported {contact['phone']}: {response.status_code}")
        except Exception as e:
            print(f"Error importing {contact['phone']}: {e}")

if __name__ == "__main__":
    print("Replace EXISTING_CONTACTS with your actual Tata panel contacts")
    print("Then run: python manual_import.py")
    import_contacts()