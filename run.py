#!/usr/bin/env python3
"""
LinkShield AI - Unified Launcher Script
Starts both the Flask backend and serves the frontend
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

def print_banner():
    """Print the application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██╗     ██╗███╗   ██╗██╗  ██╗███████╗██╗  ██╗██╗███████╗██╗  ║
    ║   ██║     ██║████╗  ██║██║ ██╔╝██╔════╝██║  ██║██║██╔════╝██║  ║
    ║   ██║     ██║██╔██╗ ██║█████╔╝ ███████╗███████║██║█████╗  ██║  ║
    ║   ██║     ██║██║╚██╗██║██╔═██╗ ╚════██║██╔══██║██║██╔══╝  ██║  ║
    ║   ███████╗██║██║ ╚████║██║  ██╗███████║██║  ██║██║██║     ██║  ║
    ║   ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ║
    ║                                                               ║
    ║              AI-Powered Phishing Detection System             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("\n" + "="*65)
    print("  Starting LinkShield AI...")
    print("="*65 + "\n")

def check_model_exists():
    """Check if the trained model exists"""
    model_path = Path(__file__).parent / 'backend' / 'phishing_model.pkl'
    return model_path.exists()

def train_model():
    """Train the AI model"""
    print("📚 Training AI model...")
    backend_dir = Path(__file__).parent / 'backend'
    
    try:
        result = subprocess.run(
            [sys.executable, 'train_model.py'],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Model trained successfully!\n")
            return True
        else:
            print("❌ Model training failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error training model: {e}")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("📦 Checking dependencies...")
    backend_dir = Path(__file__).parent / 'backend'
    
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'],
            cwd=backend_dir,
            check=True
        )
        print("✅ Dependencies installed!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not install dependencies: {e}")
        return False

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask backend server...")
    backend_dir = Path(__file__).parent / 'backend'
    
    # Start the Flask app in a separate process
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = 'development'
    
    try:
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd=backend_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend server started on http://localhost:5000\n")
            return process
        else:
            stdout, stderr = process.communicate()
            print("❌ Backend failed to start:")
            print(stderr)
            return None
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(3)
    print("🌐 Opening browser...")
    webbrowser.open('http://localhost:5000')

def main():
    """Main entry point"""
    print_banner()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"🐍 Python version: {sys.version.split()[0]}\n")
    
    # Install dependencies
    install_dependencies()
    
    # Check if model exists, train if not
    if not check_model_exists():
        print("🤖 AI model not found. Training new model...")
        if not train_model():
            print("❌ Failed to train model. Exiting.")
            sys.exit(1)
    else:
        print("✅ AI model found!\n")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server. Exiting.")
        sys.exit(1)
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("="*65)
    print("  🎉 LinkShield AI is running!")
    print("  📱 Open your browser: http://localhost:5000")
    print("  🛑 Press Ctrl+C to stop")
    print("="*65 + "\n")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
            # Check if backend is still running
            if backend_process.poll() is not None:
                stdout, stderr = backend_process.communicate()
                print("\n❌ Backend server stopped unexpectedly!")
                print("Error:", stderr)
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down LinkShield AI...")
        
        # Terminate backend process
        if backend_process:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        
        print("👋 Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    main()
