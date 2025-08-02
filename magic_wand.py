#!/usr/bin/env python3
"""
Magic Wand AI Tool - v1.0
A minimalist, hotkey-activated AI tool for instant text transformation.
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import pyperclip
import pynput
from pynput import keyboard
import google.generativeai as genai
import threading
import time
import os
import sys
from typing import Optional
import config

# Configure customtkinter appearance
ctk.set_appearance_mode(config.UI_THEME)
ctk.set_default_color_theme(config.UI_COLOR_THEME)

class MagicWandApp:
    def __init__(self):
        self.root = None
        self.input_frame = None
        self.input_entry = None
        self.status_label = None
        self.is_visible = False
        self.original_text = ""
        self.api_key = config.get_api_key()
        
        # Initialize Google AI
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(config.AI_MODEL)
        else:
            self.model = None
            print(f"Warning: {config.API_KEY_ENV} not found. Please set your API key.")
        
        # Start the hotkey listener
        self.listener = keyboard.GlobalHotKeys({
            config.HOTKEY: self.show_input_window
        })
        self.listener.start()
        
        # Create system tray icon (Windows)
        self.create_system_tray()
        
        print("Magic Wand AI Tool is running...")
        print(f"Press {config.HOTKEY} to activate")
        print("Press Ctrl+C to exit")
        
    def create_system_tray(self):
        """Create system tray icon for Windows"""
        try:
            import pystray
            from PIL import Image, ImageDraw
            
            # Create a simple icon
            icon_size = 64
            image = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Draw a simple wand icon
            draw.ellipse([8, 8, 24, 24], fill='#4CAF50')  # Handle
            draw.rectangle([20, 20, 56, 28], fill='#FFD700')  # Wand body
            draw.polygon([52, 24, 60, 20, 56, 28], fill='#FFD700')  # Tip
            
            def on_clicked(icon, item):
                if str(item) == "Exit":
                    icon.stop()
                    os._exit(0)
                elif str(item) == "Show":
                    self.show_input_window()
            
            menu = pystray.Menu(
                pystray.MenuItem("Show Magic Wand", on_clicked),
                pystray.MenuItem("Exit", on_clicked)
            )
            
            self.icon = pystray.Icon("MagicWand", image, "Magic Wand AI", menu)
            threading.Thread(target=self.icon.run, daemon=True).start()
            
        except ImportError:
            print("pystray not available, running without system tray")
        except Exception as e:
            print(f"System tray creation failed: {e}")
    
    def show_input_window(self):
        """Show the minimalist input window"""
        if self.is_visible:
            return
            
        self.is_visible = True
        
        # Get the currently highlighted text
        self.original_text = pyperclip.paste()
        
        # Create the input window
        self.root = ctk.CTkToplevel()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (config.WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (config.WINDOW_HEIGHT // 2)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}")
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
        # Create the input frame
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title label
        title_label = ctk.CTkLabel(
            self.input_frame, 
            text="✨ Magic Wand AI", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Input entry
        self.input_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text=config.INPUT_PLACEHOLDER,
            font=ctk.CTkFont(size=12)
        )
        self.input_entry.pack(fill="x", padx=20, pady=10)
        self.input_entry.focus()
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.input_frame,
            text=config.STATUS_READY,
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.status_label.pack(pady=5)
        
        # Bind events
        self.input_entry.bind('<Return>', self.process_command)
        self.input_entry.bind('<Escape>', self.hide_window)
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Focus the input
        self.input_entry.focus()
        
    def hide_window(self, event=None):
        """Hide the input window"""
        if self.root:
            self.root.destroy()
            self.root = None
        self.is_visible = False
        
    def process_command(self, event=None):
        """Process the user's command"""
        command = self.input_entry.get().strip()
        if not command:
            return
            
        self.status_label.configure(text=config.STATUS_PROCESSING, text_color="orange")
        self.root.update()
        
        # Process in a separate thread to avoid blocking the UI
        threading.Thread(target=self._process_command_async, args=(command,), daemon=True).start()
        
    def _process_command_async(self, command):
        """Process the command asynchronously"""
        try:
            if not self.model:
                self._update_status(config.STATUS_ERROR, "red")
                return
                
            # Create the prompt
            prompt = config.PROMPT_TEMPLATE.format(
                command=command,
                text=self.original_text
            )
            
            # Get response from AI
            response = self.model.generate_content(prompt)
            transformed_text = response.text.strip()
            
            # Copy the result to clipboard
            pyperclip.copy(transformed_text)
            
            # Update status
            self._update_status(config.STATUS_SUCCESS, "green")
            
            # Auto-hide after configured delay
            threading.Timer(config.AUTO_HIDE_DELAY, self.hide_window).start()
            
        except Exception as e:
            self._update_status(f"Error: {str(e)}", "red")
            
    def _update_status(self, message, color):
        """Update the status label from the main thread"""
        if self.root:
            self.root.after(0, lambda: self.status_label.configure(text=message, text_color=color))
            
    def run(self):
        """Run the application"""
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down Magic Wand...")
            if hasattr(self, 'icon'):
                self.icon.stop()
            self.listener.stop()
            sys.exit(0)

def main():
    """Main entry point"""
    print("Starting Magic Wand AI Tool...")
    print(f"Make sure you have set the {config.API_KEY_ENV} environment variable")
    
    # Print configuration summary
    config.print_config_summary()
    
    app = MagicWandApp()
    app.run()

if __name__ == "__main__":
    main() 