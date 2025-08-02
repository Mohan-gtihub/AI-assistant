# 🔧 Troubleshooting Guide

## Common Installation Issues

### Python 3.13 Compatibility Issues

If you're using Python 3.13 and getting build errors, try these solutions:

#### Solution 1: Use Alternative Installation Script
```bash
python install_dependencies.py
```

#### Solution 2: Manual Installation
Install packages one by one:
```bash
pip install customtkinter
pip install pyperclip
pip install pynput
pip install google-generativeai
pip install pystray
pip install Pillow
pip install python-dotenv
```

#### Solution 3: Downgrade Python
If issues persist, consider using Python 3.11 or 3.12:
1. Download Python 3.11 from https://python.org/downloads/
2. Create a virtual environment: `python -m venv magic_wand_env`
3. Activate it: `magic_wand_env\Scripts\activate` (Windows) or `source magic_wand_env/bin/activate` (macOS)
4. Install dependencies: `pip install -r requirements.txt`

### API Key Issues

#### Error: "API key not found"
1. Get your API key from https://makersuite.google.com/app/apikey
2. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-api-key-here"
   
   # Windows Command Prompt
   set GEMINI_API_KEY=your-api-key-here
   
   # macOS/Linux
   export GEMINI_API_KEY="your-api-key-here"
   ```

#### Error: "Invalid API key"
1. Make sure you copied the entire API key
2. Check that there are no extra spaces
3. Verify the API key is active in Google AI Studio

### Hotkey Issues

#### Error: "Hotkey not working"
1. Make sure no other application uses `Ctrl+Alt+A`
2. Try a different hotkey by editing `config.py`:
   ```python
   HOTKEY = '<ctrl>+<alt>+s'  # Change to Ctrl+Alt+S
   ```

#### Error: "Permission denied" (Windows)
1. Run as Administrator
2. Check Windows Defender settings
3. Add the application to Windows Firewall exceptions

### GUI Issues

#### Error: "customtkinter not found"
```bash
pip install customtkinter
```

#### Error: "Tkinter not available"
1. Install tkinter (usually comes with Python)
2. On Ubuntu/Debian: `sudo apt-get install python3-tk`
3. On macOS: `brew install python-tk`

### Clipboard Issues

#### Error: "pyperclip not working"
```bash
pip install pyperclip
```

#### Error: "Clipboard access denied"
1. Check if another application is using the clipboard
2. Restart the application
3. On Windows, try running as Administrator

## Quick Fix Commands

### Windows
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python install_dependencies.py

# Set API key
$env:GEMINI_API_KEY="your-api-key-here"

# Run application
python start_magic_wand.py
```

### macOS
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
python3 install_dependencies.py

# Set API key
export GEMINI_API_KEY="your-api-key-here"

# Run application
python3 start_magic_wand.py
```

## Testing Your Installation

Run the test script to verify everything works:
```bash
python test_magic_wand.py
```

## Getting Help

If you're still having issues:

1. **Check Python version**: `python --version`
2. **Check installed packages**: `pip list`
3. **Run test script**: `python test_magic_wand.py`
4. **Check error logs**: Look for error messages in the console

## Common Error Messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `python install_dependencies.py` |
| `PermissionError` | Run as Administrator (Windows) or with sudo (macOS) |
| `KeyError: '__version__'` | Use `python install_dependencies.py` |
| `subprocess-exited-with-error` | Try manual installation or downgrade Python |
| `API key not found` | Set `GEMINI_API_KEY` environment variable |
| `Hotkey not working` | Check if another app uses the same hotkey | 