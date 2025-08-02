#!/usr/bin/env python3
"""
Alternative dependency installation script for Magic Wand AI Tool
Handles Python 3.13 compatibility issues
"""
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Python 3.13 detected - using alternative installation method")
        return "3.13"
    
    print("✅ Python version is compatible")
    return True

def install_package(package, version=None):
    """Install a single package with error handling"""
    try:
        if version:
            cmd = [sys.executable, "-m", "pip", "install", f"{package}>={version}"]
        else:
            cmd = [sys.executable, "-m", "pip", "install", package]
        
        print(f"📦 Installing {package}...")
        subprocess.check_call(cmd)
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing {package}: {e}")
        return False

def install_dependencies_alternative():
    """Install dependencies using alternative method for Python 3.13"""
    print("🔧 Using alternative installation method for Python 3.13...")
    
    packages = [
        ("customtkinter", "5.2.0"),
        ("pyperclip", "1.8.0"),
        ("pynput", "1.7.0"),
        ("google-generativeai", "0.8.0"),
        ("pystray", "0.19.0"),
        ("Pillow", "10.0.0"),
        ("python-dotenv", "1.0.0")
    ]
    
    failed_packages = []
    
    for package, version in packages:
        if not install_package(package, version):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Some packages failed to install: {', '.join(failed_packages)}")
        print("Trying alternative installation methods...")
        
        # Try installing without version constraints
        for package in failed_packages:
            print(f"🔄 Retrying {package} without version constraint...")
            if install_package(package):
                failed_packages.remove(package)
    
    if failed_packages:
        print(f"\n❌ Failed to install: {', '.join(failed_packages)}")
        print("Please try manual installation:")
        for package in failed_packages:
            print(f"pip install {package}")
        return False
    
    print("✅ All dependencies installed successfully!")
    return True

def install_dependencies_standard():
    """Install dependencies using standard method"""
    print("📦 Installing dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("⬆️  Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not upgrade pip: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Magic Wand AI Tool - Dependency Installation")
    print("=" * 50)
    
    # Check Python version
    python_status = check_python_version()
    if python_status is False:
        return
    
    # Upgrade pip first
    upgrade_pip()
    
    # Install dependencies based on Python version
    if python_status == "3.13":
        success = install_dependencies_alternative()
    else:
        success = install_dependencies_standard()
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Get your API key from https://makersuite.google.com/app/apikey")
        print("2. Set the environment variable: GEMINI_API_KEY=your_key_here")
        print("3. Run the application: python start_magic_wand.py")
    else:
        print("\n❌ Installation failed. Please try manual installation:")
        print("pip install customtkinter pyperclip pynput google-generativeai pystray Pillow python-dotenv")

if __name__ == "__main__":
    main() 