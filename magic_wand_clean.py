#!/usr/bin/env python3
"""
Ultimate AI Windows Assistant - All-in-One Companion
A powerful AI assistant that can actually control your system, launch apps, browse web, and more.
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
import requests
import json
import re
from datetime import datetime
import psutil
import win32gui
import win32con
import win32api
from pathlib import Path
import sqlite3
import hashlib
import winreg
import socket
import speedtest
from PIL import Image, ImageTk
import cv2
import numpy as np
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import schedule
import pyautogui
import speech_recognition as sr
import pyttsx3
from plyer import notification
import qrcode
from io import BytesIO
import base64

# Configure customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AdvancedSystemController:
    """Advanced system operations and utilities"""
    
    @staticmethod
    def get_wifi_passwords():
        """Get saved WiFi passwords"""
        try:
            profiles = []
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="ignore").split('\n')
            for line in data:
                if "All User Profile" in line:
                    wifi_name = line.split(":")[1][1:-1]
                    try:
                        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', wifi_name, 'key=clear']).decode('utf-8', errors="ignore").split('\n')
                        for result in results:
                            if "Key Content" in result:
                                password = result.split(":")[1][1:-1]
                                profiles.append(f"📶 {wifi_name}: {password}")
                                break
                    except:
                        profiles.append(f"📶 {wifi_name}: [No password saved]")
            return "\n".join(profiles) if profiles else "No WiFi profiles found"
        except Exception as e:
            return f"❌ Error retrieving WiFi passwords: {str(e)}"
    
    @staticmethod
    def network_speed_test():
        """Test internet speed"""
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000
            ping = st.results.ping
            
            return f"""🌐 Network Speed Test Results:
📥 Download: {download_speed:.2f} Mbps
📤 Upload: {upload_speed:.2f} Mbps
⚡ Ping: {ping:.2f} ms"""
        except Exception as e:
            return f"❌ Speed test failed: {str(e)}"
    
    @staticmethod
    def take_screenshot(save_path=None):
        """Take a screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            if save_path:
                screenshot.save(save_path)
                return f"📸 Screenshot saved to: {save_path}"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                default_path = f"screenshot_{timestamp}.png"
                screenshot.save(default_path)
                return f"📸 Screenshot saved as: {default_path}"
        except Exception as e:
            return f"❌ Screenshot failed: {str(e)}"
    
    @staticmethod
    def generate_qr_code(text):
        """Generate QR code for text"""
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_code_{timestamp}.png"
            img.save(filename)
            return f"📱 QR code generated: {filename}"
        except Exception as e:
            return f"❌ QR generation failed: {str(e)}"
    
    @staticmethod
    def send_notification(title, message):
        """Send system notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
            return f"🔔 Notification sent: {title}"
        except Exception as e:
            return f"❌ Notification failed: {str(e)}"
    
    @staticmethod
    def get_installed_programs():
        """Get list of installed programs"""
        try:
            programs = []
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                try:
                    subkey_name = winreg.EnumKey(reg_key, i)
                    subkey = winreg.OpenKey(reg_key, subkey_name)
                    try:
                        program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        programs.append(program_name)
                    except FileNotFoundError:
                        pass
                    winreg.CloseKey(subkey)
                except WindowsError:
                    pass
            
            winreg.CloseKey(reg_key)
            programs.sort()
            return f"💻 Installed Programs ({len(programs)} found):\n" + "\n".join(f"• {prog}" for prog in programs[:20]) + ("\n... and more" if len(programs) > 20 else "")
        except Exception as e:
            return f"❌ Error getting programs: {str(e)}"
    
    @staticmethod
    def empty_recycle_bin():
        """Empty the recycle bin"""
        try:
            subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'], check=True)
            return "🗑️ Recycle bin emptied successfully"
        except Exception as e:
            return f"❌ Failed to empty recycle bin: {str(e)}"
    
    @staticmethod
    def get_battery_info():
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "🔌 Plugged in" if battery.power_plugged else "🔋 On battery"
                time_left = f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "∞"
                return f"🔋 Battery: {percent}% | {plugged} | Time left: {time_left}"
            else:
                return "🖥️ Desktop computer (no battery)"
        except Exception as e:
            return f"❌ Battery info unavailable: {str(e)}"

class VoiceAssistant:
    """Voice recognition and text-to-speech capabilities"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.setup_voice()
    
    def setup_voice(self):
        """Configure voice settings"""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Use female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume
        except Exception as e:
            print(f"Voice setup error: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return "🔊 Speech completed"
        except Exception as e:
            return f"❌ Speech failed: {str(e)}"
    
    def listen(self):
        """Listen for voice input"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            text = self.recognizer.recognize_google(audio)
            return f"🎤 Heard: {text}", text
        except sr.WaitTimeoutError:
            return "⏰ Listening timeout", None
        except sr.UnknownValueError:
            return "❓ Could not understand audio", None
        except Exception as e:
            return f"❌ Voice recognition error: {str(e)}", None

class EmailManager:
    """Email operations"""
    
    @staticmethod
    def send_email(to_email, subject, body, smtp_server="smtp.gmail.com", smtp_port=587, from_email=None, password=None):
        """Send email (requires configuration)"""
        try:
            if not from_email or not password:
                return "❌ Email credentials not configured. Set SMTP_EMAIL and SMTP_PASSWORD environment variables."
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            
            return f"📧 Email sent to {to_email}"
        except Exception as e:
            return f"❌ Email failed: {str(e)}"

class SmartScheduler:
    """Task scheduling and reminders"""
    
    def __init__(self):
        self.scheduled_tasks = []
    
    def add_reminder(self, message, when):
        """Add a reminder"""
        try:
            # Simple time parsing (extend as needed)
            if 'minute' in when:
                minutes = int(re.findall(r'\d+', when)[0])
                schedule.every(minutes).minutes.do(self.show_reminder, message)
            elif 'hour' in when:
                hours = int(re.findall(r'\d+', when)[0])
                schedule.every(hours).hours.do(self.show_reminder, message)
            
            return f"⏰ Reminder set: {message} in {when}"
        except Exception as e:
            return f"❌ Reminder failed: {str(e)}"
    
    def show_reminder(self, message):
        """Show reminder notification"""
        AdvancedSystemController.send_notification("Reminder", message)
        return schedule.CancelJob  # Remove after showing
    
    def run_pending(self):
        """Run pending scheduled tasks"""
        schedule.run_pending()

class SystemController:
    """Handles all system-level operations"""
    
    @staticmethod
    def open_application(app_name):
        """Launch applications by name"""
        app_paths = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'edge': 'msedge.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'task manager': 'taskmgr.exe',
            'control panel': 'control.exe',
            'settings': 'ms-settings:',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
            'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
            'vscode': r'C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe'.format(os.getenv('USERNAME')),
            'discord': r'C:\Users\{}\AppData\Local\Discord\Update.exe --processStart Discord.exe'.format(os.getenv('USERNAME')),
            'spotify': r'C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe'.format(os.getenv('USERNAME')),
            'vlc': r'C:\Program Files\VideoLAN\VLC\vlc.exe',
        }
        
        app_name = app_name.lower()
        if app_name in app_paths:
            try:
                subprocess.Popen(app_paths[app_name], shell=True)
                return f"✅ Opened {app_name.title()}"
            except Exception as e:
                return f"❌ Failed to open {app_name}: {str(e)}"
        else:
            # Try to find and launch by searching
            try:
                subprocess.Popen(f'start "" "{app_name}"', shell=True)
                return f"✅ Attempted to open {app_name}"
            except Exception as e:
                return f"❌ Application '{app_name}' not found"
    
    @staticmethod
    def web_search(query):
        """Perform web search"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"🔍 Searched for: {query}"
    
    @staticmethod
    def open_website(url):
        """Open website in default browser"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)
        return f"🌐 Opened: {url}"
    
    @staticmethod
    def system_info():
        """Get system information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"""💻 System Information:
CPU Usage: {cpu_percent}%
RAM: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
Platform: {sys.platform}"""
        return info
    
    @staticmethod
    def kill_process(process_name):
        """Kill a process by name"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    return f"✅ Killed process: {proc.info['name']}"
            return f"❌ Process '{process_name}' not found"
        except Exception as e:
            return f"❌ Error killing process: {str(e)}"
    
    @staticmethod
    def create_file(filename, content=""):
        """Create a new file"""
        try:
            with open(filename, 'w') as f:
                f.write(content)
            return f"✅ Created file: {filename}"
        except Exception as e:
            return f"❌ Error creating file: {str(e)}"
    
    @staticmethod
    def shutdown_system(action="shutdown"):
        """Shutdown, restart, or sleep the system"""
        commands = {
            'shutdown': 'shutdown /s /t 10',
            'restart': 'shutdown /r /t 10',
            'sleep': 'powercfg -h off && rundll32.exe powrprof.dll,SetSuspendState 0,1,0',
            'hibernate': 'shutdown /h'
        }
        
        if action in commands:
            try:
                subprocess.run(commands[action], shell=True)
                return f"✅ System will {action} in 10 seconds"
            except Exception as e:
                return f"❌ Error: {str(e)}"
        return f"❌ Unknown action: {action}"

class AIProcessor:
    """Advanced AI processing with multiple capabilities"""
    
    def __init__(self):
        self.setup_ai()
        self.command_history = []
        self.setup_database()
        self.voice_assistant = VoiceAssistant()
        self.scheduler = SmartScheduler()
    
    def setup_database(self):
        """Setup local database for learning user preferences"""
        try:
            self.db_path = os.path.join(os.path.expanduser("~"), ".magic_wand_db.sqlite")
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY,
                    command TEXT,
                    response TEXT,
                    timestamp DATETIME,
                    success BOOLEAN
                )
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Database setup error: {e}")
            self.conn = None
    
    def setup_ai(self):
        """Setup AI model"""
        try:
            import google.generativeai as genai
            api_key = os.getenv('GEMINI_API_KEY')
            
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-pro")
                print("✅ Google AI configured")
            else:
                self.model = None
                print("⚠️  No API key found - using advanced demo mode")
        except ImportError:
            self.model = None
            print("⚠️  Google AI not available - using advanced demo mode")
        except Exception as e:
            self.model = None
            print(f"❌ AI setup failed: {e}")
    
    def process_command(self, command, selected_text=""):
        """Process commands with AI and system integration"""
        command_lower = command.lower()
        
        # System control commands
        if any(word in command_lower for word in ['open', 'launch', 'start', 'run']):
            return self.handle_app_launch(command)
        
        elif any(word in command_lower for word in ['search', 'google', 'find']):
            return self.handle_search(command)
        
        elif any(word in command_lower for word in ['website', 'browse', 'go to']):
            return self.handle_website(command)
        
        elif 'system info' in command_lower or 'system status' in command_lower:
            return SystemController.system_info()
        
        elif any(word in command_lower for word in ['kill', 'close', 'stop']):
            return self.handle_kill_process(command)
        
        elif any(word in command_lower for word in ['shutdown', 'restart', 'sleep', 'hibernate']):
            return self.handle_power_command(command)
        
        elif any(word in command_lower for word in ['create file', 'new file', 'make file']):
            return self.handle_create_file(command)
        
        # Advanced system commands
        elif 'wifi password' in command_lower or 'wifi info' in command_lower:
            return AdvancedSystemController.get_wifi_passwords()
        
        elif 'speed test' in command_lower or 'network speed' in command_lower:
            return AdvancedSystemController.network_speed_test()
        
        elif 'screenshot' in command_lower:
            return AdvancedSystemController.take_screenshot()
        
        elif 'qr code' in command_lower:
            text_to_encode = command.replace('qr code', '').replace('generate', '').strip()
            if not text_to_encode and selected_text:
                text_to_encode = selected_text
            return AdvancedSystemController.generate_qr_code(text_to_encode or "Hello World")
        
        elif 'installed programs' in command_lower or 'list programs' in command_lower:
            return AdvancedSystemController.get_installed_programs()
        
        elif 'empty recycle bin' in command_lower or 'clear trash' in command_lower:
            return AdvancedSystemController.empty_recycle_bin()
        
        elif 'battery' in command_lower or 'power status' in command_lower:
            return AdvancedSystemController.get_battery_info()
        
        # Voice commands
        elif 'speak' in command_lower or 'say' in command_lower:
            text_to_speak = command.replace('speak', '').replace('say', '').strip()
            if not text_to_speak and selected_text:
                text_to_speak = selected_text
            return self.voice_assistant.speak(text_to_speak or "Hello, I am your AI assistant")
        
        elif 'listen' in command_lower or 'voice input' in command_lower:
            result, text = self.voice_assistant.listen()
            if text:
                # Process the voice command
                return f"{result}\nProcessing voice command: {self.process_command(text, selected_text)}"
            return result
        
        # Email commands
        elif 'send email' in command_lower:
            return self.handle_email_command(command)
        
        # Reminder commands
        elif 'remind me' in command_lower or 'set reminder' in command_lower:
            return self.handle_reminder_command(command)
        
        elif 'notification' in command_lower:
            return self.handle_notification_command(command)
        
        # Text processing commands
        elif selected_text:
            return self.handle_text_processing(command, selected_text)
        
        # General AI commands
        else:
            return self.handle_general_ai(command)
    
    def handle_app_launch(self, command):
        """Handle application launching"""
        # Extract app name from command
        patterns = [
            r'(?:open|launch|start|run)\s+(.+)',
            r'(.+)\s+(?:open|launch|start|run)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                app_name = match.group(1).strip()
                return SystemController.open_application(app_name)
        
        return "❌ Please specify which application to open"
    
    def handle_search(self, command):
        """Handle web searches"""
        patterns = [
            r'(?:search|google|find)\s+(?:for\s+)?(.+)',
            r'(.+)\s+(?:search|google)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                return SystemController.web_search(query)
        
        return "❌ Please specify what to search for"
    
    def handle_website(self, command):
        """Handle website opening"""
        patterns = [
            r'(?:website|browse|go to)\s+(.+)',
            r'open\s+(.+\.(?:com|org|net|edu|gov))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                url = match.group(1).strip()
                return SystemController.open_website(url)
        
        return "❌ Please specify which website to open"
    
    def handle_kill_process(self, command):
        """Handle process killing"""
        patterns = [
            r'(?:kill|close|stop)\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                process_name = match.group(1).strip()
                return SystemController.kill_process(process_name)
        
        return "❌ Please specify which process to kill"
    
    def handle_power_command(self, command):
        """Handle power management"""
        if 'shutdown' in command.lower():
            return SystemController.shutdown_system('shutdown')
        elif 'restart' in command.lower():
            return SystemController.shutdown_system('restart')
        elif 'sleep' in command.lower():
            return SystemController.shutdown_system('sleep')
        elif 'hibernate' in command.lower():
            return SystemController.shutdown_system('hibernate')
        
        return "❌ Unknown power command"
    
    def handle_create_file(self, command):
        """Handle file creation"""
        patterns = [
            r'(?:create|new|make)\s+file\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                filename = match.group(1).strip()
                return SystemController.create_file(filename)
        
        return "❌ Please specify filename"
    
    def handle_email_command(self, command):
        """Handle email sending"""
        # Simple email parsing - extend as needed
        if 'to' in command and 'subject' in command:
            # Parse email components (basic implementation)
            return "📧 Email feature requires SMTP configuration. Set SMTP_EMAIL and SMTP_PASSWORD environment variables."
        return "❌ Email format: 'send email to user@example.com subject Hello body How are you?'"
    
    def handle_reminder_command(self, command):
        """Handle reminder setting"""
        # Extract reminder details
        message_match = re.search(r'remind me (?:to )?(.+?) in (\d+ \w+)', command, re.IGNORECASE)
        if message_match:
            message, when = message_match.groups()
            return self.scheduler.add_reminder(message, when)
        return "❌ Reminder format: 'remind me to call John in 30 minutes'"
    
    def handle_notification_command(self, command):
        """Handle notification sending"""
        # Extract title and message
        parts = command.replace('notification', '').strip().split(':', 1)
        if len(parts) == 2:
            title, message = parts
            return AdvancedSystemController.send_notification(title.strip(), message.strip())
        else:
            message = parts[0] if parts else "Test notification"
            return AdvancedSystemController.send_notification("AI Assistant", message)
    
    def handle_text_processing(self, command, text):
        """Handle text processing with AI"""
        if self.model:
            try:
                prompt = f"""
You are an advanced AI assistant integrated into Windows. Process this text according to the user's command.

Command: {command}
Text to process: {text}

Provide the transformed text only, no explanations unless specifically asked.
"""
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                return f"❌ AI Error: {str(e)}"
        else:
            # Advanced demo responses
            demo_responses = {
                'fix grammar': self.fix_grammar_demo(text),
                'make professional': self.make_professional_demo(text),
                'summarize': self.summarize_demo(text),
                'translate': self.translate_demo(command, text),
                'explain': self.explain_demo(text),
                'rewrite': self.rewrite_demo(text),
                'bullet points': self.bullet_points_demo(text),
                'expand': self.expand_demo(text),
                'simplify': self.simplify_demo(text),
            }
            
            for key, func in demo_responses.items():
                if key in command.lower():
                    return func
            
            return f"Demo: Processed '{command}' on {len(text)} characters of text"
    
    def handle_general_ai(self, command):
        """Handle general AI queries"""
        if self.model:
            try:
                response = self.model.generate_content(command)
                return response.text.strip()
            except Exception as e:
                return f"❌ AI Error: {str(e)}"
        else:
            return self.generate_smart_demo_response(command)
    
    def fix_grammar_demo(self, text):
        """Demo grammar fixing"""
        # Simple demo - fix common issues
        fixed = text.replace(" i ", " I ")
        fixed = re.sub(r'\bi\b', 'I', fixed)
        fixed = re.sub(r'\.{2,}', '.', fixed)
        return f"Grammar-corrected: {fixed}"
    
    def make_professional_demo(self, text):
        """Demo professional rewriting"""
        return f"Professional version: {text.replace('!', '.').replace('...', '.')}"
    
    def summarize_demo(self, text):
        """Demo summarization"""
        words = text.split()
        if len(words) > 20:
            summary = ' '.join(words[:15]) + "... [Summary of remaining content]"
        else:
            summary = f"Brief summary: {text[:50]}..."
        return summary
    
    def translate_demo(self, command, text):
        """Demo translation"""
        if 'spanish' in command.lower():
            return f"Spanish: [Traducción de demostración del texto]"
        elif 'french' in command.lower():
            return f"French: [Traduction de démonstration du texte]"
        else:
            return f"Translation demo: [Translated version of the text]"
    
    def explain_demo(self, text):
        """Demo explanation"""
        return f"Explanation: This text discusses {text[:30]}... [AI would provide detailed explanation]"
    
    def rewrite_demo(self, text):
        """Demo rewriting"""
        return f"Rewritten: {text} [AI would provide alternative phrasing]"
    
    def bullet_points_demo(self, text):
        """Demo bullet points conversion"""
        return f"• Key point from the text\n• Another important aspect\n• Summary conclusion"
    
    def expand_demo(self, text):
        """Demo text expansion"""
        return f"{text} [AI would add relevant details, examples, and elaboration to make this more comprehensive]"
    
    def simplify_demo(self, text):
        """Demo text simplification"""
        return f"Simplified: {text[:30]}... [AI would use simpler words and shorter sentences]"
    
    def generate_smart_demo_response(self, command):
        """Generate intelligent demo responses"""
        responses = {
            'weather': "🌤️ Demo: Today's weather is sunny, 75°F. [Real version would show actual weather]",
            'time': f"🕐 Current time: {datetime.now().strftime('%I:%M %p')}",
            'date': f"📅 Today's date: {datetime.now().strftime('%B %d, %Y')}",
            'joke': "😄 Why don't scientists trust atoms? Because they make up everything!",
            'reminder': "⏰ Demo: Reminder set! [Real version would integrate with system notifications]",
            'calculate': "🔢 Demo: Mathematical calculation result [Real version would compute actual math]",
            'password': "🔐 Demo: SecurePass123! [Real version would generate cryptographically secure passwords]",
            'email': "📧 Demo: Email draft created [Real version would integrate with email clients]",
            'screenshot': "📸 Demo: Screenshot taken [Real version would capture actual screen]",
            'battery': "🔋 Demo: Battery at 85%, 4h 30m remaining [Real version shows actual battery status]",
            'wifi': "📶 Demo: WiFi passwords retrieved [Real version shows actual saved passwords]",
            'speed test': "🌐 Demo: Download: 150 Mbps, Upload: 50 Mbps [Real version tests actual speed]",
            'voice': "🎤 Demo: Voice recognition active [Real version uses microphone]",
            'qr': "📱 Demo: QR code generated [Real version creates actual QR codes]",
        }
        
        for key, response in responses.items():
            if key in command.lower():
                return response
        
        return f"🤖 AI Demo Response: I understand you want to '{command}'. In the full version, I would provide a comprehensive AI-generated response with real system integration."
    
    def save_to_history(self, command, response, success=True):
        """Save command to history database"""
        if self.conn:
            try:
                self.conn.execute(
                    "INSERT INTO command_history (command, response, timestamp, success) VALUES (?, ?, ?, ?)",
                    (command, response, datetime.now(), success)
                )
                self.conn.commit()
            except Exception as e:
                print(f"History save error: {e}")

class UltimateAIAssistant:
    def __init__(self):
        print("🚀 Initializing Ultimate AI Windows Assistant...")
        
        # Create hidden root window
        self.hidden_root = ctk.CTk()
        self.hidden_root.withdraw()
        
        self.spotlight_window = None
        self.input_entry = None
        self.status_label = None
        self.output_text = None
        self.is_visible = False
        self.original_text = ""
        self.listener = None
        
        # Initialize components
        self.ai_processor = AIProcessor()
        self._setup_hotkey()
        
        # Start background scheduler
        self._start_scheduler_thread()
        
        print("✅ Ultimate AI Assistant initialized!")
        print("🎯 Press Ctrl+Alt+A to activate AI Assistant")
        print("💡 NEW Features: Voice control, screenshots, QR codes, WiFi passwords, speed tests!")
        
    def _start_scheduler_thread(self):
        """Start background thread for scheduled tasks"""
        def scheduler_loop():
            while True:
                self.ai_processor.scheduler.run_pending()
                time.sleep(1)
        
        scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        scheduler_thread.start()
        
    def _setup_hotkey(self):
        """Setup global hotkey listener"""
        try:
            from pynput import keyboard
            self.listener = keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+a': self.show_spotlight
            })
            self.listener.start()
            print("✅ Hotkey active: Ctrl+Alt+A")
        except ImportError:
            print("❌ pynput not available")
            self.listener = None
        except Exception as e:
            print(f"❌ Hotkey setup failed: {e}")
            self.listener = None
    
    def show_spotlight(self):
        """Show the AI Assistant interface"""
        if self.is_visible:
            if self.spotlight_window:
                self.spotlight_window.lift()
                self.spotlight_window.focus_force()
            return
            
        self.is_visible = True
        
        # Get clipboard content
        try:
            self.original_text = pyperclip.paste()
        except:
            self.original_text = ""
        
        # Create enhanced UI
        try:
            self.spotlight_window = ctk.CTkToplevel(self.hidden_root)
            self.spotlight_window.title("Ultimate AI Assistant")
            self.spotlight_window.geometry("800x500")
            self.spotlight_window.resizable(True, True)
            
            # Center window
            self.spotlight_window.update_idletasks()
            screen_width = self.spotlight_window.winfo_screenwidth()
            screen_height = self.spotlight_window.winfo_screenheight()
            x = (screen_width // 2) - 400
            y = (screen_height // 2) - 250
            self.spotlight_window.geometry(f"800x500+{x}+{y}")
            
            self.spotlight_window.attributes('-topmost', True)
            self.spotlight_window.lift()
            self.spotlight_window.focus_force()
            
            # Create main container
            main_frame = ctk.CTkFrame(self.spotlight_window, fg_color="transparent")
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title section
            title_frame = ctk.CTkFrame(main_frame, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
            title_frame.pack(fill="x", pady=(0, 15))
            
            title_content = ctk.CTkFrame(title_frame, fg_color="transparent")
            title_content.pack(fill="x", padx=20, pady=15)
            
            # AI Assistant header
            header_frame = ctk.CTkFrame(title_content, fg_color="transparent")
            header_frame.pack(fill="x")
            header_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(
                header_frame,
                text="🤖",
                font=ctk.CTkFont(size=32),
                text_color="#00D4AA"
            ).grid(row=0, column=0, padx=(0, 15))
            
            ctk.CTkLabel(
                header_frame,
                text="Ultimate AI Assistant",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=("#ffffff", "#ffffff")
            ).grid(row=0, column=1, sticky="w")
            
            # Capabilities display
            caps_label = ctk.CTkLabel(
                title_content,
                text="🚀 Apps • 🌐 Web • 💻 System • ✍️ Text • 🧠 AI • 🎤 Voice • 📸 Screenshot • 📶 WiFi • 🔋 Battery • 📱 QR",
                font=ctk.CTkFont(size=12),
                text_color="#888888"
            )
            caps_label.pack(pady=(10, 0))
            
            # Input section
            input_frame = ctk.CTkFrame(main_frame, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
            input_frame.pack(fill="x", pady=(0, 15))
            
            input_content = ctk.CTkFrame(input_frame, fg_color="transparent")
            input_content.pack(fill="x", padx=20, pady=15)
            input_content.grid_columnconfigure(0, weight=1)
            
            self.input_entry = ctk.CTkEntry(
                input_content,
                placeholder_text="Try: 'screenshot', 'wifi passwords', 'speed test', 'speak hello', 'qr code', 'battery info'...",
                font=ctk.CTkFont(size=16),
                height=45,
                fg_color=("#3a3a3a", "#2a2a2a"),
                border_color=("#00D4AA", "#00A085"),
                border_width=2
            )
            self.input_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
            
            process_btn = ctk.CTkButton(
                input_content,
                text="Execute",
                command=self.process_command,
                width=100,
                height=45,
                fg_color=("#00D4AA", "#00A085"),
                hover_color=("#00A085", "#007A5E"),
                font=ctk.CTkFont(size=14, weight="bold")
            )
            process_btn.grid(row=0, column=1)
            
            # Output section
            output_frame = ctk.CTkFrame(main_frame, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
            output_frame.pack(fill="both", expand=True, pady=(0, 15))
            
            output_content = ctk.CTkFrame(output_frame, fg_color="transparent")
            output_content.pack(fill="both", expand=True, padx=20, pady=15)
            
            ctk.CTkLabel(
                output_content,
                text="📤 Response:",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#00D4AA"
            ).pack(anchor="w", pady=(0, 10))
            
            self.output_text = ctk.CTkTextbox(
                output_content,
                font=ctk.CTkFont(size=13),
                fg_color=("#3a3a3a", "#2a2a2a"),
                text_color=("#ffffff", "#ffffff"),
                wrap="word"
            )
            self.output_text.pack(fill="both", expand=True)
            
            # Status bar
            self.status_label = ctk.CTkLabel(
                main_frame,
                text="🟢 Ready • Press Enter to execute • Esc to close",
                font=ctk.CTkFont(size=12),
                text_color="#888888"
            )
            self.status_label.pack(pady=(0, 0))
            
            # Bind events
            self.input_entry.bind('<Return>', self.process_command)
            self.input_entry.bind('<Escape>', self.hide_spotlight)
            self.spotlight_window.protocol("WM_DELETE_WINDOW", self.hide_spotlight)
            
            # Focus input
            self.spotlight_window.after(100, self._focus_input)
            
            # Show welcome message
            self.output_text.insert("1.0", 
                "🎉 Welcome to your Ultimate AI Assistant! 🚀\n\n"
                "🆕 NEW ADVANCED FEATURES:\n"
                "• 🎤 Voice Control: 'listen' or 'speak hello world'\n"
                "• 📸 Screenshots: 'screenshot' or 'take screenshot'\n"
                "• 📶 WiFi Info: 'wifi passwords' to see saved networks\n"
                "• 🌐 Speed Test: 'speed test' for internet speed\n"
                "• 📱 QR Codes: 'qr code your text here'\n"
                "• 🔋 Battery: 'battery info' for power status\n"
                "• 🗑️ Cleanup: 'empty recycle bin'\n"
                "• 💻 Programs: 'list installed programs'\n"
                "• 🔔 Notifications: 'notification title: message'\n"
                "• ⏰ Reminders: 'remind me to call John in 30 minutes'\n\n"
                "CLASSIC FEATURES:\n"
                "• 🚀 Launch apps: 'open chrome', 'start notepad'\n"
                "• 🌐 Web control: 'search Python tutorials', 'go to github.com'\n"
                "• 💻 System info: 'system info', 'kill chrome', 'shutdown'\n"
                "• ✍️ Text processing: Select text + 'fix grammar', 'translate'\n"
                "• 🤖 AI chat: Ask me anything!\n\n"
                "Try: 'screenshot' or 'speed test' to see advanced features!"
            )
            
            print("✅ AI Assistant interface ready")
            
        except Exception as e:
            print(f"❌ Error creating interface: {e}")
            import traceback
            traceback.print_exc()
            self.is_visible = False
    
    def _focus_input(self):
        """Focus the input field"""
        try:
            self.input_entry.focus_set()
            self.input_entry.focus_force()
        except:
            pass
    
    def process_command(self, event=None):
        """Process user command"""
        if not self.input_entry:
            return
            
        command = self.input_entry.get().strip()
        if not command:
            return

        # Update status
        self.status_label.configure(text="🔄 Processing...", text_color="#FFA500")
        self.input_entry.configure(state="disabled")
        
        # Clear previous output
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", "Processing your request...\n")
        
        # Process in background
        threading.Thread(target=self._process_async, args=(command,), daemon=True).start()
    
    def _process_async(self, command):
        """Process command asynchronously"""
        try:
            print(f"🎯 Processing: {command}")
            
            # Process with AI
            response = self.ai_processor.process_command(command, self.original_text)
            
            # Save to history
            self.ai_processor.save_to_history(command, response, True)
            
            # Update UI on main thread
            self.hidden_root.after(0, lambda: self._update_output(response, command))
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(f"❌ Processing error: {e}")
            self.hidden_root.after(0, lambda: self._update_output(error_msg, command))
    
    def _update_output(self, response, command):
        """Update output display"""
        try:
            if self.output_text:
                self.output_text.delete("1.0", tk.END)
                
                # Format output nicely
                output = f"Command: {command}\n"
                output += "=" * 50 + "\n\n"
                output += response
                
                self.output_text.insert("1.0", output)
                
                # Copy to clipboard if it's text processing
                if self.original_text and any(word in command.lower() for word in ['fix', 'translate', 'rewrite', 'grammar']):
                    pyperclip.copy(response)
                    self.status_label.configure(text="✅ Done! Result copied to clipboard", text_color="#4CAF50")
                else:
                    self.status_label.configure(text="✅ Command executed successfully", text_color="#4CAF50")
            
            # Re-enable input
            if self.input_entry:
                self.input_entry.configure(state="normal")
                self.input_entry.delete(0, tk.END)
                self.input_entry.focus_set()
            
        except Exception as e:
            print(f"❌ Error updating output: {e}")
    
    def hide_spotlight(self, event=None):
        """Hide the assistant window"""
        if self.spotlight_window:
            try:
                self.spotlight_window.destroy()
            except:
                pass
        
        if self.hidden_root:
            try:
                self.hidden_root.quit()
                self.hidden_root.destroy()
            except:
                pass
        
        sys.exit(0)
    
    def run(self):
        """Run the application"""
        try:
            self.hidden_root.mainloop()
        except KeyboardInterrupt:
            self.shutdown()
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown"""
        print("🛑 Shutting down Ultimate AI Assistant...")
        
        if self.listener:
            try:
                self.listener.stop()
            except:
                pass
        
        if self.ai_processor.conn:
            try:
                self.ai_processor.conn.close()
            except:
                pass
        
        if self.spotlight_window:
            try:
                self.spotlight_window.destroy()
            except:
                pass
        
        if self.hidden_root:
            try:
                self.hidden_root.quit()
                self.hidden_root.destroy()
            except:
                pass
        
        sys.exit(0)

def main():
    """Main entry point"""
    print("🚀 Starting Ultimate AI Windows Assistant...")
    print("=" * 60)
    print("🎯 Features:")
    print("   • 🚀 Launch any Windows application")
    print("   • 🌐 Browse websites and perform web searches")
    print("   • 💻 Control system (shutdown, restart, kill processes)")
    print("   • 📝 Advanced text processing with AI")
    print("   • 🤖 Natural language AI chat")
    print("   • 📊 System monitoring and information")
    print("   • 📁 File operations")
    print("=" * 60)
    
    # Check for required dependencies
    missing_deps = []
    try:
        import customtkinter
    except ImportError:
        missing_deps.append("customtkinter")
    
    try:
        import pyperclip
    except ImportError:
        missing_deps.append("pyperclip")
    
    try:
        import psutil
    except ImportError:
        missing_deps.append("psutil")
    
    try:
        import win32gui
    except ImportError:
        missing_deps.append("pywin32")
    
    try:
        from pynput import keyboard
    except ImportError:
        missing_deps.append("pynput")
    
    try:
        import pyttsx3
    except ImportError:
        missing_deps.append("pyttsx3")
    
    try:
        import speech_recognition
    except ImportError:
        missing_deps.append("SpeechRecognition")
    
    try:
        import speedtest
    except ImportError:
        missing_deps.append("speedtest-cli")
    
    try:
        import pyautogui
    except ImportError:
        missing_deps.append("pyautogui")
    
    try:
        import qrcode
    except ImportError:
        missing_deps.append("qrcode[pil]")
    
    try:
        import plyer
    except ImportError:
        missing_deps.append("plyer")
    
    try:
        import schedule
    except ImportError:
        missing_deps.append("schedule")
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n📦 Install with: pip install " + " ".join(missing_deps))
        input("Press Enter to continue anyway (some features may not work)...")
    
    try:
        app = UltimateAIAssistant()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
def main():
    """Main entry point"""
    print("🚀 Starting Ultimate AI Windows Assistant...")
    print("=" * 60)
    print("🎯 Features:")
    print("   • 🚀 Launch any Windows application")
    print("   • 🌐 Browse websites and perform web searches")
    print("   • 💻 Control system (shutdown, restart, kill processes)")
    print("   • 📝 Advanced text processing with AI")
    print("   • 🤖 Natural language AI chat")
    print("   • 📊 System monitoring and information")
    print("   • 📁 File operations")
    print("   • 🎤 Voice control and text-to-speech")
    print("   • 📸 Screenshots and QR code generation")
    print("   • 📶 WiFi management and speed testing")
    print("   • 🔔 Smart notifications and reminders")
    print("=" * 60)
    
    # Check for required dependencies
    missing_deps = []
    try:
        import customtkinter
    except ImportError:
        missing_deps.append("customtkinter")
    
    try:
        import pyperclip
    except ImportError:
        missing_deps.append("pyperclip")
    
    try:
        import psutil
    except ImportError:
        missing_deps.append("psutil")
    
    try:
        import win32gui
    except ImportError:
        missing_deps.append("pywin32")
    
    try:
        from pynput import keyboard
    except ImportError:
        missing_deps.append("pynput")
    
    try:
        import pyttsx3
    except ImportError:
        missing_deps.append("pyttsx3")
    
    try:
        import speech_recognition
    except ImportError:
        missing_deps.append("SpeechRecognition")
    
    try:
        import speedtest
    except ImportError:
        missing_deps.append("speedtest-cli")
    
    try:
        import pyautogui
    except ImportError:
        missing_deps.append("pyautogui")
    
    try:
        import qrcode
    except ImportError:
        missing_deps.append("qrcode[pil]")
    
    try:
        import plyer
    except ImportError:
        missing_deps.append("plyer")
    
    try:
        import schedule
    except ImportError:
        missing_deps.append("schedule")
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n📦 Install with: pip install " + " ".join(missing_deps))
        input("Press Enter to continue anyway (some features may not work)...")
    
    try:
        app = UltimateAIAssistant()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()