from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('static', 'dashboard.html')

@app.route('/api/send-template', methods=['POST'])
def send_template():
    data = request.get_json()
    phone = data.get('phone')
    return jsonify({'success': True, 'message': f'Template sent to {phone}!'})

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    phone = data.get('phone')
    message = data.get('message')
    return jsonify({'success': True, 'message': f'Message sent to {phone}!'})

@app.route('/api/chats')
def get_chats():
    return jsonify({'chats': [], 'stats': {'totalMessages': 0, 'activeChats': 0, 'aiResponses': 0}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)