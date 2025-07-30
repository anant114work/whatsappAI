#!/usr/bin/env python3
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True

def run_server():
    """Run the Flask server"""
    try:
        print("Starting WhatsApp OpenAI Bot...")
        print("Phone Number: +919355421616")
        print("AI Model: GPT-4o-mini")
        print("Server: http://localhost:3000")
        print("Webhook: http://localhost:3000/webhook")
        print("\n" + "="*50)
        
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == "__main__":
    print("Setting up WhatsApp OpenAI Bot...")
    
    if install_requirements():
        run_server()
    else:
        print("Setup failed. Please check the error messages above.")