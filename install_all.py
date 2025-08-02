#!/usr/bin/env python3
"""
Ultimate AI Assistant - Complete Installation Script
Installs all dependencies and sets up the application
"""

import subprocess
import sys
import os
import platform

def print_header():
    print("🚀 Ultimate AI Assistant - Installation Script")
    print("=" * 60)
    print("This script will install all required dependencies")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("\n📦 Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to upgrade pip: {e}")
        return False

def install_package(package, description=""):
    """Install a single package"""
    try:
        print(f"📦 Installing {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {package} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {package}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing {package}: {e}")
        return False

def install_core_dependencies():
    """Install core dependencies"""
    print("\n🔧 Installing core dependencies...")
    
    core_packages = [
        "customtkinter>=5.2.0",
        "pyperclip>=1.8.0", 
        "pynput>=1.7.0",
        "google-generativeai>=0.8.0"
    ]
    
    success_count = 0
    for package in core_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Core dependencies: {success_count}/{len(core_packages)} installed")
    return success_count == len(core_packages)

def install_system_dependencies():
    """Install system control dependencies"""
    print("\n💻 Installing system control dependencies...")
    
    system_packages = [
        "psutil>=5.9.0",
        "pywin32>=306"
    ]
    
    success_count = 0
    for package in system_packages:
        if install_package(package):
            success_count += 1
    
    print(f"📊 System dependencies: {success_count}/{len(system_packages)} installed")
    return success_count == len(system_packages)

def install_voice_dependencies():
    """Install voice recognition dependencies"""
    print("\n🎤 Installing voice recognition dependencies...")
    
    voice_packages = [
        "pyttsx3>=2.90",
        "SpeechRecognition>=3.10.0"
    ]
    
    success_count = 0
    for package in voice_packages:
        if install_package(package):
            success_count += 1
    
    # Try to install pyaudio (optional)
    try:
        install_package("pyaudio")
        print("✅ pyaudio installed (voice features enhanced)")
    except:
        print("⚠️  pyaudio not installed (voice features may be limited)")
    
    print(f"📊 Voice dependencies: {success_count}/{len(voice_packages)} installed")
    return success_count == len(voice_packages)

def install_advanced_dependencies():
    """Install advanced feature dependencies"""
    print("\n🚀 Installing advanced feature dependencies...")
    
    advanced_packages = [
        "pyautogui>=0.9.54",
        "speedtest-cli>=2.1.3",
        "qrcode[pil]>=7.4.2",
        "plyer>=2.1.0",
        "schedule>=1.2.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "opencv-python>=4.8.0"
    ]
    
    success_count = 0
    for package in advanced_packages:
        if install_package(package):
            success_count += 1
    
    print(f"📊 Advanced dependencies: {success_count}/{len(advanced_packages)} installed")
    return success_count == len(advanced_packages)

def test_installation():
    """Test if all components work"""
    print("\n🧪 Testing installation...")
    
    tests = [
        ("customtkinter", "GUI framework"),
        ("pyperclip", "Clipboard operations"),
        ("pynput", "Hotkey detection"),
        ("psutil", "System monitoring"),
        ("pyttsx3", "Text-to-speech"),
        ("pyautogui", "Screenshot capability"),
        ("qrcode", "QR code generation"),
        ("plyer", "System notifications")
    ]
    
    passed = 0
    total = len(tests)
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"✅ {description} - OK")
            passed += 1
        except ImportError:
            print(f"❌ {description} - FAILED")
    
    print(f"\n📊 Installation test: {passed}/{total} components working")
    return passed == total

def create_quick_start_script():
    """Create a quick start script"""
    script_content = '''@echo off
echo 🚀 Starting Ultimate AI Assistant...
python magic_wand_clean.py
pause
'''
    
    try:
        with open("start_assistant.bat", "w") as f:
            f.write(script_content)
        print("✅ Created start_assistant.bat - Double-click to run!")
    except Exception as e:
        print(f"❌ Could not create start script: {e}")

def main():
    """Main installation process"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Upgrade pip
    upgrade_pip()
    
    # Install dependencies
    core_ok = install_core_dependencies()
    system_ok = install_system_dependencies()
    voice_ok = install_voice_dependencies()
    advanced_ok = install_advanced_dependencies()
    
    # Test installation
    test_ok = test_installation()
    
    # Create quick start script
    create_quick_start_script()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Installation Complete!")
    print("=" * 60)
    
    if test_ok:
        print("✅ All components installed successfully!")
        print("\n🚀 To start the Ultimate AI Assistant:")
        print("   1. Run: python magic_wand_clean.py")
        print("   2. Press Ctrl+Alt+A to activate")
        print("   3. Or double-click: start_assistant.bat")
        
        print("\n🎯 Try these commands:")
        print("   • 'open notepad'")
        print("   • 'search for Python tutorials'")
        print("   • 'screenshot'")
        print("   • 'wifi passwords'")
        print("   • 'speed test'")
        print("   • 'speak hello world'")
        
    else:
        print("⚠️  Some components failed to install")
        print("   The app will work with limited features")
        print("   Try running: python test.py to see what works")
    
    print("\n💡 Pro Tips:")
    print("   • The app runs in background - press Ctrl+Alt+A to activate")
    print("   • Get API key from https://makersuite.google.com/app/apikey for full AI features")
    print("   • Run as Administrator if some features don't work")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 