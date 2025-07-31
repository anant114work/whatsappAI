try:
    from flask import Flask, request, jsonify
    print("✅ Flask imported")
    
    import requests
    print("✅ Requests imported")
    
    import os
    print("✅ OS imported")
    
    from datetime import datetime
    print("✅ Datetime imported")
    
    from dotenv import load_dotenv
    print("✅ Dotenv imported")
    
    from openai import OpenAI
    print("✅ OpenAI imported")
    
    load_dotenv()
    print("✅ Environment loaded")
    
    app = Flask(__name__)
    print("✅ Flask app created")
    
    @app.route('/api/send-template', methods=['POST'])
    def test_route():
        return jsonify({'success': True})
    
    print("✅ Route registered")
    print("All imports successful - your main app should work")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("This is why your main app fails")