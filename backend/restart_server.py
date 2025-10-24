#!/usr/bin/env python3
"""
Backend server restart script for Skill Gap Analyzer
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

def find_backend_process():
    """Find running backend process"""
    try:
        # On Windows, use tasklist
        if os.name == 'nt':
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                                  capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'python.exe' in line and 'uvicorn' in line:
                    # Extract PID
                    parts = line.split()
                    if len(parts) > 1:
                        return int(parts[1])
        else:
            # On Unix-like systems, use ps
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'uvicorn' in line and 'app.main:app' in line:
                    parts = line.split()
                    if len(parts) > 1:
                        return int(parts[1])
    except Exception as e:
        print(f"Error finding process: {e}")
    return None

def kill_backend_process(pid):
    """Kill the backend process"""
    try:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(pid), '/F'], check=True)
        else:
            os.kill(pid, signal.SIGTERM)
        print(f"✅ Killed backend process {pid}")
        return True
    except Exception as e:
        print(f"❌ Error killing process {pid}: {e}")
        return False

def start_backend_server():
    """Start the backend server"""
    try:
        backend_dir = Path(__file__).parent
        os.chdir(backend_dir)
        
        print("🚀 Starting backend server...")
        subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--reload', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ])
        
        print("✅ Backend server started!")
        print("📡 Server running at: http://localhost:8000")
        print("📚 API docs at: http://localhost:8000/docs")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    print("🔄 Restarting Skill Gap Analyzer Backend Server")
    print("=" * 50)
    
    # Find and kill existing process
    pid = find_backend_process()
    if pid:
        print(f"🔍 Found running backend process: {pid}")
        if kill_backend_process(pid):
            print("⏳ Waiting for process to terminate...")
            time.sleep(2)
    else:
        print("ℹ️  No running backend process found")
    
    # Start new server
    if start_backend_server():
        print("\n🎉 Backend server restarted successfully!")
        print("\n📋 Next steps:")
        print("1. Test the registration endpoint:")
        print("   curl -X POST http://localhost:8000/api/v1/auth/register \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"username\":\"test\",\"email\":\"test@example.com\",\"password\":\"TestPass123\",\"confirm_password\":\"TestPass123\"}'")
        print("\n2. Check the frontend registration form")
        print("\n3. View API documentation at: http://localhost:8000/docs")
    else:
        print("\n💥 Failed to restart backend server!")
        sys.exit(1)

if __name__ == "__main__":
    main()
