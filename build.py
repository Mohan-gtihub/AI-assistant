#!/usr/bin/env python3
"""
Build script for Magic Wand AI Tool
Creates executables for Windows and macOS
"""

import os
import sys
import subprocess
import platform
import shutil

def check_dependencies():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller is installed")
        return True
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing PyInstaller: {e}")
            return False

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}")

def build_windows():
    """Build Windows executable"""
    print("🔨 Building Windows executable...")
    try:
        # Use the spec file for better control
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller", 
            "magic_wand.spec",
            "--clean"
        ])
        
        # Check if executable was created
        exe_path = os.path.join("dist", "MagicWand.exe")
        if os.path.exists(exe_path):
            print(f"✅ Windows executable created: {exe_path}")
            return True
        else:
            print("❌ Windows executable not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building Windows executable: {e}")
        return False

def build_macos():
    """Build macOS application"""
    print("🔨 Building macOS application...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "magic_wand.py",
            "--onefile",
            "--windowed",
            "--name=MagicWand",
            "--clean"
        ])
        
        # Check if app was created
        app_path = os.path.join("dist", "MagicWand")
        if os.path.exists(app_path):
            print(f"✅ macOS application created: {app_path}")
            return True
        else:
            print("❌ macOS application not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building macOS application: {e}")
        return False

def build_linux():
    """Build Linux executable"""
    print("🔨 Building Linux executable...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "magic_wand.py",
            "--onefile",
            "--name=MagicWand",
            "--clean"
        ])
        
        # Check if executable was created
        exe_path = os.path.join("dist", "MagicWand")
        if os.path.exists(exe_path):
            print(f"✅ Linux executable created: {exe_path}")
            return True
        else:
            print("❌ Linux executable not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building Linux executable: {e}")
        return False

def create_installer_script():
    """Create installer script for the built executable"""
    current_os = platform.system()
    
    if current_os == "Windows":
        installer_content = """@echo off
echo Installing Magic Wand AI Tool...
echo.
echo This will copy the executable to your desktop for easy access.
echo.

set "source=%~dp0dist\\MagicWand.exe"
set "desktop=%USERPROFILE%\\Desktop\\MagicWand.exe"

if exist "%source%" (
    copy "%source%" "%desktop%"
    echo ✅ Magic Wand installed to desktop!
    echo.
    echo To run: Double-click MagicWand.exe on your desktop
    echo To uninstall: Delete MagicWand.exe from your desktop
) else (
    echo ❌ MagicWand.exe not found in dist folder
    echo Please run the build script first.
)

pause
"""
        with open("install.bat", "w") as f:
            f.write(installer_content)
        print("✅ Windows installer script created: install.bat")
        
    elif current_os == "Darwin":
        installer_content = """#!/bin/bash
echo "Installing Magic Wand AI Tool..."
echo ""
echo "This will copy the application to your Applications folder."
echo ""

source="$(dirname "$0")/dist/MagicWand"
destination="/Applications/MagicWand"

if [ -f "$source" ]; then
    cp "$source" "$destination"
    chmod +x "$destination"
    echo "✅ Magic Wand installed to Applications!"
    echo ""
    echo "To run: Open MagicWand from Applications folder"
    echo "To uninstall: Delete MagicWand from Applications folder"
else
    echo "❌ MagicWand not found in dist folder"
    echo "Please run the build script first."
fi

read -p "Press Enter to continue..."
"""
        with open("install.command", "w") as f:
            f.write(installer_content)
        os.chmod("install.command", 0o755)
        print("✅ macOS installer script created: install.command")

def main():
    """Main build function"""
    print("🔨 Magic Wand AI Tool Builder")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build for current platform
    current_os = platform.system()
    success = False
    
    if current_os == "Windows":
        success = build_windows()
    elif current_os == "Darwin":
        success = build_macos()
    elif current_os == "Linux":
        success = build_linux()
    else:
        print(f"❌ Unsupported operating system: {current_os}")
        sys.exit(1)
    
    if success:
        print("\n🎉 Build completed successfully!")
        create_installer_script()
        
        print(f"\n📦 Files created:")
        if current_os == "Windows":
            print("   - dist/MagicWand.exe (Windows executable)")
            print("   - install.bat (Windows installer)")
        elif current_os == "Darwin":
            print("   - dist/MagicWand (macOS application)")
            print("   - install.command (macOS installer)")
        elif current_os == "Linux":
            print("   - dist/MagicWand (Linux executable)")
        
        print("\n📋 Next steps:")
        print("1. Set your GEMINI_API_KEY environment variable")
        print("2. Run the installer script or copy the executable to your desired location")
        print("3. Launch the application and press Ctrl+Alt+A to activate!")
        
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 