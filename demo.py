#!/usr/bin/env python3
"""
Demo script for Magic Wand AI Tool
This script demonstrates the core functionality with sample text transformations
"""

import os
import sys
import config
import google.generativeai as genai

def demo_text_transformations():
    """Demonstrate various text transformations"""
    print("✨ Magic Wand AI Tool - Demo")
    print("=" * 50)
    
    # Sample texts and commands
    demos = [
        {
            "name": "Code Refactoring",
            "text": "def calculate_sum(a,b):\n    return a+b",
            "command": "refactor this code with proper documentation and type hints"
        },
        {
            "name": "Text Translation",
            "text": "Hello, how are you today?",
            "command": "translate to Spanish"
        },
        {
            "name": "Email Writing",
            "text": "meeting tomorrow, 2pm, discuss project timeline",
            "command": "convert this to a professional email"
        },
        {
            "name": "Code Documentation",
            "text": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
            "command": "add comprehensive documentation to this function"
        },
        {
            "name": "Data Format Conversion",
            "text": '{"name": "John", "age": 30, "city": "New York"}',
            "command": "convert this JSON to a Python dictionary with proper formatting"
        }
    ]
    
    # Test API connection first
    api_key = config.get_api_key()
    if not api_key:
        print("❌ No API key found. Please set the GEMINI_API_KEY environment variable.")
        print("Get your free API key from: https://makersuite.google.com/app/apikey")
        return False
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(config.AI_MODEL)
        print("✅ API connection established")
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False
    
    print(f"\n🎯 Running {len(demos)} demo transformations...")
    print("=" * 50)
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{i}. {demo['name']}")
        print("-" * 30)
        print(f"📝 Original Text:")
        print(demo['text'])
        print(f"\n🎯 Command: {demo['command']}")
        
        try:
            # Create the prompt
            prompt = config.PROMPT_TEMPLATE.format(
                command=demo['command'],
                text=demo['text']
            )
            
            # Get AI response
            response = model.generate_content(prompt)
            transformed_text = response.text.strip()
            
            print(f"\n✨ Transformed Result:")
            print(transformed_text)
            print("✅ Success!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
    
    return True

def demo_usage_workflow():
    """Demonstrate the typical usage workflow"""
    print("\n🎮 Typical Usage Workflow")
    print("=" * 50)
    
    steps = [
        "1. Start the Magic Wand application",
        "2. Select any text in any application",
        "3. Press Ctrl+Alt+A to activate",
        "4. Type your transformation command",
        "5. Press Enter and wait for the result",
        "6. Press Ctrl+V to paste the transformed text"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n💡 Example Commands:")
    example_commands = [
        "refactor this code",
        "add documentation",
        "translate to French",
        "make this more professional",
        "explain this in simple terms",
        "convert to JSON",
        "summarize this",
        "fix grammar and spelling"
    ]
    
    for cmd in example_commands:
        print(f"   • \"{cmd}\"")
    
    print("\n🚀 Ready to transform your text!")

def demo_configuration():
    """Show current configuration"""
    print("\n🔧 Current Configuration")
    print("=" * 50)
    
    config.print_config_summary()

def main():
    """Main demo function"""
    print("🧪 Magic Wand AI Tool - Demo Mode")
    print("This demo shows the core functionality without running the full application.")
    print()
    
    # Show configuration
    demo_configuration()
    
    # Run text transformations
    if demo_text_transformations():
        # Show usage workflow
        demo_usage_workflow()
        
        print("\n🎉 Demo completed!")
        print("\n📋 Next steps:")
        print("1. Set your GEMINI_API_KEY environment variable")
        print("2. Run: python magic_wand.py")
        print("3. Start transforming text with Ctrl+Alt+A!")
    else:
        print("\n❌ Demo failed. Please check your API key and try again.")

if __name__ == "__main__":
    main() 