#!/usr/bin/env python3
"""
Setup script for Magic Wand AI Tool
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_api_key():
    """Guide user through API key setup"""
    print("\n🔑 Setting up Google AI Gemini API Key")
    print("1. Go to https://makersuite.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Copy the API key")
    
    api_key = input("\nEnter your API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  No API key provided. You'll need to set it manually later.")
        print("   Set the GEMINI_API_KEY environment variable before running the app.")
        return False
    
    # Set environment variable for current session
    os.environ['GEMINI_API_KEY'] = api_key
    
    # Create a .env file for future sessions
    try:
        with open('.env', 'w') as f:
            f.write(f'GEMINI_API_KEY={api_key}\n')
        print("✅ API key saved to .env file")
        return True
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False

def create_startup_script():
    """Create a startup script for easy launching"""
    script_content = """#!/usr/bin/env python3
import os
import sys

# Load environment variables from .env file
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Import and run the application
from magic_wand import main

if __name__ == "__main__":
    main()
"""
    
    try:
        with open('start_magic_wand.py', 'w') as f:
            f.write(script_content)
        print("✅ Startup script created: start_magic_wand.py")
        return True
    except Exception as e:
        print(f"❌ Error creating startup script: {e}")
        return False

def create_windows_batch():
    """Create a Windows batch file for easy launching"""
    if platform.system() == "Windows":
        batch_content = """@echo off
echo Starting Magic Wand AI Tool...
python start_magic_wand.py
pause
"""
        try:
            with open('start_magic_wand.bat', 'w') as f:
                f.write(batch_content)
            print("✅ Windows batch file created: start_magic_wand.bat")
            return True
        except Exception as e:
            print(f"❌ Error creating batch file: {e}")
            return False
    return True

def create_macos_script():
    """Create a macOS script for easy launching"""
    if platform.system() == "Darwin":
        script_content = """#!/bin/bash
echo "Starting Magic Wand AI Tool..."
python3 start_magic_wand.py
"""
        try:
            with open('start_magic_wand.command', 'w') as f:
                f.write(script_content)
            os.chmod('start_magic_wand.command', 0o755)
            print("✅ macOS script created: start_magic_wand.command")
            return True
        except Exception as e:
            print(f"❌ Error creating macOS script: {e}")
            return False
    return True

def main():
    """Main setup function"""
    print("✨ Magic Wand AI Tool Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup API key
    setup_api_key()
    
    # Create startup scripts
    create_startup_script()
    create_windows_batch()
    create_macos_script()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. If you didn't set an API key, get one from https://makersuite.google.com/app/apikey")
    print("2. Set the GEMINI_API_KEY environment variable")
    print("3. Run the application:")
    
    if platform.system() == "Windows":
        print("   - Double-click start_magic_wand.bat")
        print("   - Or run: python start_magic_wand.py")
    elif platform.system() == "Darwin":
        print("   - Double-click start_magic_wand.command")
        print("   - Or run: python3 start_magic_wand.py")
    else:
        print("   - Run: python3 start_magic_wand.py")
    
    print("\n🎮 Usage:")
    print("- Press Ctrl+Alt+A to activate the Magic Wand")
    print("- Select text, give a command, and see the magic happen!")
    print("- Press Ctrl+C to exit")

if __name__ == "__main__":
    main() 