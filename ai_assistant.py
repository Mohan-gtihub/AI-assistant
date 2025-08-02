#!/usr/bin/env python3
"""
AI Assistant - Your Personal Computer AI
A comprehensive AI assistant that can do anything on your computer.
"""

import tkinter as tk
import customtkinter as ctk
import pyperclip
import threading
import time
import os
import sys
import subprocess
import webbrowser
import platform
import json
from datetime import datetime

# Configure customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AIAssistant:
    def __init__(self):
        print("🔧 Initializing AI Assistant...")
        
        # Create hidden root window first
        self.hidden_root = ctk.CTk()
        self.hidden_root.withdraw()  # Hide the main window
        
        self.assistant_window = None
        self.input_entry = None
        self.status_label = None
        self.chat_display = None
        self.is_visible = False
        self.chat_history = []
        self.listener = None
        
        # Initialize hotkey listener
        self._setup_hotkey()
        
        # Initialize AI model
        self._setup_ai()
        
        # Initialize system info
        self.system_info = self._get_system_info()
        
        print("✅ AI Assistant initialized successfully!")
        print("Press Ctrl+Alt+A to activate")
        print("Press Ctrl+C to exit")
        
    def _setup_hotkey(self):
        """Setup global hotkey listener"""
        try:
            from pynput import keyboard
            print("🔧 Setting up hotkey listener...")
            
            self.listener = keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+a': self.show_assistant
            })
            self.listener.start()
            print("✅ Hotkey listener started (Ctrl+Alt+A)")
            
        except ImportError:
            print("❌ pynput not available - hotkey disabled")
            self.listener = None
        except Exception as e:
            print(f"❌ Hotkey setup failed: {e}")
            self.listener = None
    
    def _setup_ai(self):
        """Setup AI model"""
        try:
            import google.generativeai as genai
            api_key = os.getenv('GEMINI_API_KEY')
            
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                print("✅ Google AI configured with API key")
            else:
                self.model = None
                print("⚠️  No API key found - using demo mode")
                
        except ImportError:
            self.model = None
            print("⚠️  Google AI not available - using demo mode")
        except Exception as e:
            self.model = None
            print(f"❌ AI setup failed: {e} - using demo mode")
    
    def _get_system_info(self):
        """Get system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "username": os.getenv('USERNAME', os.getenv('USER', 'Unknown')),
            "home_dir": os.path.expanduser("~"),
            "current_dir": os.getcwd()
        }
    
    def show_assistant(self):
        """Show the AI Assistant interface"""
        print("🎯 Showing AI Assistant...")
        
        if self.is_visible:
            print("⚠️  Assistant already visible")
            if self.assistant_window:
                self.assistant_window.lift()
                self.assistant_window.focus_force()
            return
            
        self.is_visible = True
        
        # Create the Assistant window
        try:
            self.assistant_window = ctk.CTkToplevel(self.hidden_root)
            self.assistant_window.title("AI Assistant")
            
            # Set window properties
            self.assistant_window.geometry("800x600")
            self.assistant_window.resizable(True, True)
            
            # Center the window
            self.assistant_window.update_idletasks()
            screen_width = self.assistant_window.winfo_screenwidth()
            screen_height = self.assistant_window.winfo_screenheight()
            x = (screen_width // 2) - 400
            y = (screen_height // 2) - 300
            self.assistant_window.geometry(f"800x600+{x}+{y}")
            
            # Make window always on top and focus
            self.assistant_window.attributes('-topmost', True)
            self.assistant_window.lift()
            self.assistant_window.focus_force()
            
            # Create main frame
            main_frame = ctk.CTkFrame(self.assistant_window)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create header
            header_frame = ctk.CTkFrame(main_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            
            title_label = ctk.CTkLabel(
                header_frame,
                text="🤖 AI Assistant",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#FFD700"
            )
            title_label.pack(side="left", padx=10, pady=10)
            
            # Create chat display
            chat_frame = ctk.CTkFrame(main_frame)
            chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Chat display (scrollable text area)
            self.chat_display = ctk.CTkTextbox(
                chat_frame,
                font=ctk.CTkFont(size=12),
                wrap="word"
            )
            self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Input frame
            input_frame = ctk.CTkFrame(main_frame)
            input_frame.pack(fill="x", padx=10, pady=(5, 10))
            
            # Input entry
            self.input_entry = ctk.CTkEntry(
                input_frame,
                placeholder_text="Ask me anything! (e.g., 'open notepad', 'search for files', 'what can you do?')",
                font=ctk.CTkFont(size=14),
                height=40
            )
            self.input_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
            
            # Send button
            send_button = ctk.CTkButton(
                input_frame,
                text="Send",
                command=self.process_command,
                width=80,
                height=40
            )
            send_button.pack(side="right", padx=(5, 10), pady=10)
            
            # Status label
            self.status_label = ctk.CTkLabel(
                main_frame,
                text="Ready • Press Enter to send • Esc to close",
                font=ctk.CTkFont(size=10),
                text_color="#888888"
            )
            self.status_label.pack(pady=(0, 5))
            
            # Bind events
            self.input_entry.bind('<Return>', self.process_command)
            self.input_entry.bind('<Escape>', self.hide_assistant)
            self.assistant_window.protocol("WM_DELETE_WINDOW", self.hide_assistant)
            
            # Focus the input
            self.assistant_window.after(100, self._focus_input)
            
            # Add welcome message
            self._add_message("AI Assistant", "Hello! I'm your AI assistant. I can help you with anything on your computer. Try asking me to:\n• Open applications\n• Search for files\n• Get system information\n• Control your computer\n• Answer questions\n\nWhat would you like me to help you with?", "assistant")
            
            print("✅ AI Assistant interface created successfully")
            
        except Exception as e:
            print(f"❌ Error creating Assistant interface: {e}")
            import traceback
            traceback.print_exc()
            self.is_visible = False
    
    def _focus_input(self):
        """Focus the input field"""
        try:
            self.input_entry.focus_set()
            self.input_entry.focus_force()
        except Exception as e:
            print(f"❌ Error focusing input: {e}")
    
    def _add_message(self, sender, message, msg_type="user"):
        """Add a message to the chat display"""
        try:
            timestamp = datetime.now().strftime("%H:%M")
            color = "#4CAF50" if msg_type == "assistant" else "#2196F3"
            
            # Add to chat history
            self.chat_history.append({
                "sender": sender,
                "message": message,
                "timestamp": timestamp,
                "type": msg_type
            })
            
            # Update display
            if self.chat_display:
                self.chat_display.insert("end", f"[{timestamp}] {sender}: ", f"timestamp")
                self.chat_display.insert("end", f"{message}\n\n", f"message")
                self.chat_display.see("end")
                
        except Exception as e:
            print(f"❌ Error adding message: {e}")
    
    def hide_assistant(self, event=None):
        """Hide the AI Assistant window"""
        print("🎪 Hiding AI Assistant...")
        
        if self.assistant_window:
            try:
                self.assistant_window.destroy()
                print("✅ Assistant window destroyed")
            except Exception as e:
                print(f"❌ Error destroying window: {e}")
            self.assistant_window = None
            
        self.is_visible = False
        
    def process_command(self, event=None):
        """Process the user's command"""
        if not self.input_entry:
            return
            
        command = self.input_entry.get().strip()
        if not command:
            print("⚠️  Empty command")
            return
            
        print(f"🎯 Processing command: {command}")
        
        # Add user message to chat
        self._add_message("You", command, "user")
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Update status
        self._update_status("Processing...", "#FFA500")
        
        # Process in a separate thread
        threading.Thread(target=self._process_command_async, args=(command,), daemon=True).start()
        
    def _process_command_async(self, command):
        """Process the command asynchronously"""
        try:
            print(f"🤖 Processing command: {command}")
            
            # Check for system commands first
            system_response = self._handle_system_commands(command)
            if system_response:
                self._add_message("AI Assistant", system_response, "assistant")
                self._update_status("Ready", "#4CAF50")
                return
            
            # Use AI for other commands
            if self.model:
                # Use real AI
                print("🤖 Using real AI model...")
                prompt = f"""
You are a helpful AI assistant that can control a computer. The user has given you a command.

User's command: {command}

System information:
- OS: {self.system_info['os']}
- Username: {self.system_info['username']}
- Current directory: {self.system_info['current_dir']}

You can help with:
1. Opening applications
2. Searching for files
3. System information
4. File operations
5. Web searches
6. General questions
7. Computer control

Please provide a helpful response. If it's a system command, explain what you would do.
"""
                response = self.model.generate_content(prompt)
                result = response.text.strip()
                print(f"✅ AI response generated: {len(result)} characters")
            else:
                # Use demo responses
                print("🎭 Using demo mode...")
                result = self._get_demo_response(command)
                print(f"✅ Demo response generated: {len(result)} characters")
            
            # Add AI response to chat
            self._add_message("AI Assistant", result, "assistant")
            
            # Update status
            self._update_status("Ready", "#4CAF50")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error processing command: {error_msg}")
            
            error_response = f"Sorry, I encountered an error: {error_msg}"
            self._add_message("AI Assistant", error_response, "assistant")
            self._update_status("Error occurred", "#FF4444")
    
    def _handle_system_commands(self, command):
        """Handle system-specific commands"""
        command_lower = command.lower()
        
        # Open applications
        if "open" in command_lower:
            apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "wordpad": "wordpad.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe"
            }
            
            for app_name, app_path in apps.items():
                if app_name in command_lower:
                    try:
                        subprocess.Popen(app_path)
                        return f"✅ Opened {app_name} for you!"
                    except Exception as e:
                        return f"❌ Error opening {app_name}: {e}"
        
        # System information
        if any(word in command_lower for word in ["system info", "system information", "computer info"]):
            info = f"""
🖥️ System Information:
• OS: {self.system_info['os']} {self.system_info['os_version']}
• Python: {self.system_info['python_version']}
• Username: {self.system_info['username']}
• Current Directory: {self.system_info['current_dir']}
• Home Directory: {self.system_info['home_dir']}
"""
            return info
        
        # What can you do
        if any(word in command_lower for word in ["what can you do", "help", "capabilities"]):
            return """
🤖 I can help you with:

📁 File Operations:
• Open applications (notepad, calculator, paint, etc.)
• Search for files
• Navigate directories

💻 System Control:
• Get system information
• Check computer status
• Control applications

🌐 Web & Information:
• Search the web
• Answer questions
• Provide information

📝 Text & Communication:
• Transform text
• Generate content
• Help with writing

🎯 Just ask me anything and I'll help you!
"""
        
        # No system command found
        return None
    
    def _get_demo_response(self, command):
        """Get demo response for commands"""
        command_lower = command.lower()
        
        if "open" in command_lower:
            return "I can help you open applications! Try saying 'open notepad' or 'open calculator'."
        
        elif "search" in command_lower:
            return "I can help you search for files and information. What would you like to search for?"
        
        elif "system" in command_lower:
            return f"Here's your system info:\n• OS: {self.system_info['os']}\n• Username: {self.system_info['username']}\n• Current directory: {self.system_info['current_dir']}"
        
        elif "help" in command_lower or "what can you do" in command_lower:
            return "I'm your AI assistant! I can help you open apps, search files, get system info, answer questions, and much more. Just ask me anything!"
        
        else:
            return f"I understand you said: '{command}'. In the full version with an API key, I would provide a detailed response to help you with this request."
    
    def _update_status(self, message, color):
        """Update the status label from the main thread"""
        if self.status_label:
            try:
                self.status_label.configure(text=message, text_color=color)
                print(f"📝 Status updated: {message}")
            except Exception as e:
                print(f"❌ Error updating status: {e}")
            
    def run(self):
        """Run the application"""
        print("🚀 Starting AI Assistant main loop...")
        
        try:
            # Use tkinter mainloop
            self.hidden_root.mainloop()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down AI Assistant...")
            self.shutdown()
        except Exception as e:
            print(f"❌ Unexpected error in main loop: {e}")
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown"""
        print("🛑 Shutting down AI Assistant...")
        
        if self.listener:
            try:
                self.listener.stop()
                print("✅ Hotkey listener stopped")
            except Exception as e:
                print(f"❌ Error stopping listener: {e}")
        
        if self.assistant_window:
            try:
                self.assistant_window.destroy()
            except Exception:
                pass
        
        if self.hidden_root:
            try:
                self.hidden_root.quit()
                self.hidden_root.destroy()
            except Exception:
                pass
        
        sys.exit(0)

def main():
    """Main entry point"""
    print("🚀 Starting AI Assistant...")
    print("=" * 50)
    
    try:
        app = AIAssistant()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 