#!/usr/bin/env python3
"""
Test script for Magic Wand AI Tool
This script tests the core functionality without requiring the full application
"""

import os
import sys
import config
import google.generativeai as genai

def test_config():
    """Test configuration settings"""
    print("🔧 Testing Configuration...")
    
    # Test configuration validation
    errors = config.validate_config()
    if errors:
        print("❌ Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Configuration is valid")
    
    # Print configuration summary
    config.print_config_summary()
    return True

def test_api_connection():
    """Test API connection"""
    print("\n🔌 Testing API Connection...")
    
    api_key = config.get_api_key()
    if not api_key:
        print("❌ No API key found")
        return False
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(config.AI_MODEL)
        
        # Test with a simple prompt
        response = model.generate_content("Say 'Hello, Magic Wand!'")
        print("✅ API connection successful")
        print(f"   Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n📦 Testing Dependencies...")
    
    required_modules = [
        'customtkinter',
        'pyperclip',
        'pynput',
        'google.generativeai',
        'PIL'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - Missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies are installed")
        return True

def test_clipboard():
    """Test clipboard functionality"""
    print("\n📋 Testing Clipboard...")
    
    try:
        import pyperclip
        
        # Test clipboard read/write
        test_text = "Magic Wand Test"
        pyperclip.copy(test_text)
        clipboard_text = pyperclip.paste()
        
        if clipboard_text == test_text:
            print("✅ Clipboard functionality working")
            return True
        else:
            print("❌ Clipboard test failed")
            return False
            
    except Exception as e:
        print(f"❌ Clipboard test failed: {e}")
        return False

def test_hotkey():
    """Test hotkey configuration"""
    print("\n⌨️  Testing Hotkey Configuration...")
    
    hotkey = config.HOTKEY
    if hotkey and '+' in hotkey:
        print(f"✅ Hotkey configured: {hotkey}")
        return True
    else:
        print("❌ Invalid hotkey configuration")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Magic Wand AI Tool - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Dependencies", test_dependencies),
        ("API Connection", test_api_connection),
        ("Clipboard", test_clipboard),
        ("Hotkey", test_hotkey)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Magic Wand is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the application.")
        return False

def main():
    """Main test function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick test - only check dependencies and config
        print("🧪 Quick Test Mode")
        test_config()
        test_dependencies()
    else:
        # Full test suite
        success = run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 