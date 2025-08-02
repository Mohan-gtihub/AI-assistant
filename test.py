#!/usr/bin/env python3
"""
Simple test for Magic Wand AI Tool
"""
import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import tkinter
        print("✅ tkinter - OK")
    except ImportError as e:
        print(f"❌ tkinter - FAILED: {e}")
        return False
    
    try:
        import customtkinter
        print("✅ customtkinter - OK")
    except ImportError as e:
        print(f"❌ customtkinter - FAILED: {e}")
        return False
    
    try:
        import pyperclip
        print("✅ pyperclip - OK")
    except ImportError as e:
        print(f"❌ pyperclip - FAILED: {e}")
        return False
    
    try:
        import pynput
        print("✅ pynput - OK")
    except ImportError as e:
        print(f"❌ pynput - FAILED: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ google-generativeai - OK")
    except ImportError as e:
        print(f"❌ google-generativeai - FAILED: {e}")
        return False
    
    return True

def test_clipboard():
    """Test clipboard functionality"""
    print("\n📋 Testing clipboard...")
    
    try:
        import pyperclip
        
        # Test clipboard access
        original = pyperclip.paste()
        test_text = "Magic Wand Test"
        pyperclip.copy(test_text)
        
        if pyperclip.paste() == test_text:
            print("✅ Clipboard read/write - OK")
            pyperclip.copy(original)  # Restore original
            return True
        else:
            print("❌ Clipboard test failed")
            return False
            
    except Exception as e:
        print(f"❌ Clipboard test failed: {e}")
        return False

def test_gui():
    """Test GUI creation"""
    print("\n🖥️  Testing GUI...")
    
    try:
        import customtkinter as ctk
        
        # Create a simple test window
        root = ctk.CTk()
        root.title("Test Window")
        root.geometry("300x200")
        
        # Add a test label
        label = ctk.CTkLabel(root, text="Magic Wand Test")
        label.pack(pady=20)
        
        # Add a close button
        def close_window():
            root.destroy()
        
        button = ctk.CTkButton(root, text="Close", command=close_window)
        button.pack(pady=10)
        
        # Set a timer to close automatically after 2 seconds
        root.after(2000, root.destroy)
        
        # Run the window
        root.mainloop()
        
        print("✅ GUI creation - OK")
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Magic Wand AI Tool - Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_clipboard,
        test_gui
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\n📋 Next steps:")
        print("1. Run the application: python magic_wand_clean.py")
        print("2. Press Ctrl+Alt+A to activate")
        print("3. Or set API key: $env:GEMINI_API_KEY='your-key-here'")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n💡 Try running: python install_dependencies.py")

if __name__ == "__main__":
    main() 