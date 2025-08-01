import subprocess
import sys
import time

def restart_app():
    print("Stopping any existing Flask processes...")
    try:
        subprocess.run(["taskkill", "/f", "/im", "python.exe"], capture_output=True)
        time.sleep(2)
    except:
        pass
    
    print("Starting Flask app...")
    subprocess.Popen([sys.executable, "app.py"])
    print("Flask app started!")

if __name__ == "__main__":
    restart_app()