#!/usr/bin/env python3
"""
LinkShield AI - Setup Script
Installs dependencies and trains the initial model
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(command, cwd=None, description=None):
    """Run a shell command and handle errors"""
    if description:
        print(f"📌 {description}...")
    
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print_header("LinkShield AI - Setup")
    
    # Get project root
    project_root = Path(__file__).parent
    backend_dir = project_root / 'backend'
    
    # Check Python version
    print(f"🐍 Python version: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    print()
    
    # Install dependencies
    print_header("Installing Dependencies")
    
    if not run_command(
        [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
        cwd=backend_dir,
        description="Installing Python packages"
    ):
        print("⚠️  Warning: Some dependencies may not have installed correctly")
    
    # Train the model
    print_header("Training AI Model")
    
    if not run_command(
        [sys.executable, 'train_model.py'],
        cwd=backend_dir,
        description="Training the phishing detection model"
    ):
        print("❌ Model training failed!")
        sys.exit(1)
    
    # Success message
    print_header("Setup Complete!")
    
    print("""
🎉 LinkShield AI has been set up successfully!

To start the application:
    python run.py

Or manually:
    cd backend
    python app.py

Then open your browser to: http://localhost:5000

📖 For more information, see README.md
""")

if __name__ == '__main__':
    main()
