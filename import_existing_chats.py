"""
Since Tata doesn't provide API to fetch existing chats, 
you need to manually add some sample data or wait for webhook data.

To get ALL your existing Tata panel chats, you would need to:
1. Export chat data from Tata panel (if available)
2. Use Tata's webhook to capture new messages
3. Manually add important contacts

This script adds some sample data for demonstration.
"""

import json

# Sample chat data (replace with your actual contacts)
sample_chats = {
    "+919876543210": {
        "lastMessage": "Hello, I need help with my order",
        "timestamp": "2025-07-30T10:30:00",
        "source": "Existing customer"
    },
    "+918765432109": {
        "lastMessage": "Thank you for the service",
        "timestamp": "2025-07-30T09:15:00", 
        "source": "Previous conversation"
    },
    "+917654321098": {
        "lastMessage": "When will my product arrive?",
        "timestamp": "2025-07-29T16:45:00",
        "source": "Support inquiry"
    }
}

sample_messages = {
    "+919876543210": [
        {"text": "Hello, I need help with my order", "type": "received", "timestamp": "2025-07-30T10:30:00"},
        {"text": "Sure! I can help you with that. What's your order number?", "type": "sent", "timestamp": "2025-07-30T10:31:00"}
    ],
    "+918765432109": [
        {"text": "Thank you for the service", "type": "received", "timestamp": "2025-07-30T09:15:00"},
        {"text": "You're welcome! Feel free to contact us anytime.", "type": "sent", "timestamp": "2025-07-30T09:16:00"}
    ]
}

print("Sample chat data created.")
print("To use this data, you would need to:")
print("1. Import this into your Flask app's chats_db and messages_db")
print("2. Or manually add your actual customer phone numbers")
print("3. Wait for webhook data to capture real conversations")

# Save to file for manual import
with open('sample_chats.json', 'w') as f:
    json.dump({'chats': sample_chats, 'messages': sample_messages}, f, indent=2)

print("Sample data saved to sample_chats.json")