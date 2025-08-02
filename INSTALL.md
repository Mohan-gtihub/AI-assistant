# 🚀 Magic Wand AI Tool - Installation Guide

This guide will walk you through installing and setting up the Magic Wand AI Tool on Windows, macOS, and Linux.

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Google AI Gemini API key** (free from [Google AI Studio](https://makersuite.google.com/app/apikey))
- **Internet connection** for API access

## 🪟 Windows Installation

### Method 1: Quick Setup (Recommended)

1. **Download the project**
   ```cmd
   git clone <repository-url>
   cd AI-assistant
   ```

2. **Run the setup script**
   ```cmd
   python setup.py
   ```

3. **Get your API key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

4. **Set the environment variable**
   ```cmd
   set GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```cmd
   python start_magic_wand.py
   ```

### Method 2: Manual Installation

1. **Install Python dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

2. **Set up your API key**
   ```cmd
   set GEMINI_API_KEY=your_api_key_here
   ```

3. **Test the installation**
   ```cmd
   python test_magic_wand.py
   ```

4. **Run the application**
   ```cmd
   python magic_wand.py
   ```

### Method 3: Build Executable

1. **Install PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

2. **Build the executable**
   ```cmd
   python build.py
   ```

3. **Install the executable**
   ```cmd
   install.bat
   ```

## 🍎 macOS Installation

### Method 1: Quick Setup

1. **Download the project**
   ```bash
   git clone <repository-url>
   cd AI-assistant
   ```

2. **Run the setup script**
   ```bash
   python3 setup.py
   ```

3. **Get your API key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

4. **Set the environment variable**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   python3 start_magic_wand.py
   ```

### Method 2: Manual Installation

1. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Set up your API key**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

3. **Test the installation**
   ```bash
   python3 test_magic_wand.py
   ```

4. **Run the application**
   ```bash
   python3 magic_wand.py
   ```

### Method 3: Build Application

1. **Install PyInstaller**
   ```bash
   pip3 install pyinstaller
   ```

2. **Build the application**
   ```bash
   python3 build.py
   ```

3. **Install the application**
   ```bash
   ./install.command
   ```

## 🐧 Linux Installation

### Method 1: Quick Setup

1. **Download the project**
   ```bash
   git clone <repository-url>
   cd AI-assistant
   ```

2. **Install system dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-tk
   ```

3. **Run the setup script**
   ```bash
   python3 setup.py
   ```

4. **Get your API key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

5. **Set the environment variable**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

6. **Run the application**
   ```bash
   python3 start_magic_wand.py
   ```

### Method 2: Manual Installation

1. **Install system dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-tk
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

4. **Test the installation**
   ```bash
   python3 test_magic_wand.py
   ```

5. **Run the application**
   ```bash
   python3 magic_wand.py
   ```

## 🔧 Configuration

### Environment Variables

Set these environment variables for persistent configuration:

**Windows:**
```cmd
setx GEMINI_API_KEY your_api_key_here
```

**macOS/Linux:**
```bash
echo 'export GEMINI_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

### Customization

Edit `config.py` to customize:
- Hotkey combination
- UI theme and colors
- Window size
- AI model selection
- System tray settings

## 🧪 Testing

Run the test suite to verify everything is working:

```bash
python test_magic_wand.py
```

Or run a quick test:
```bash
python test_magic_wand.py --quick
```

## 🎮 Usage

1. **Start the application**
   ```bash
   python magic_wand.py
   ```

2. **Select text** in any application

3. **Press the hotkey** (`Ctrl+Alt+A` by default)

4. **Type your command** (e.g., "refactor this", "translate to Spanish")

5. **Press Enter** and see the magic happen!

6. **Paste the result** with `Ctrl+V`

## 🐛 Troubleshooting

### Common Issues

**"API key not configured"**
- Make sure you've set the `GEMINI_API_KEY` environment variable
- Restart the application after setting the key

**"Hotkey not working"**
- Ensure the application has permission to listen for global hotkeys
- Try running as administrator on Windows
- Check if another application is using the same hotkey

**"System tray not showing"**
- Install `pystray` and `Pillow`: `pip install pystray Pillow`
- Some Linux distributions may require additional packages

**"ImportError: No module named 'customtkinter'"**
- Install dependencies: `pip install -r requirements.txt`

**"Permission denied" (Linux)**
- Install system dependencies: `sudo apt-get install python3-tk`
- Grant necessary permissions for global hotkeys

### Debug Mode

Run with verbose output:
```bash
python magic_wand.py --debug
```

### Getting Help

1. **Check the logs** for error messages
2. **Run the test suite** to identify issues
3. **Check your API key** is valid
4. **Verify dependencies** are installed correctly

## 📦 Building from Source

### Prerequisites for Building

**Windows:**
- Python 3.8+
- PyInstaller: `pip install pyinstaller`

**macOS:**
- Python 3.8+
- PyInstaller: `pip3 install pyinstaller`

**Linux:**
- Python 3.8+
- PyInstaller: `pip3 install pyinstaller`
- Additional packages: `sudo apt-get install build-essential`

### Build Commands

**Windows:**
```cmd
python build.py
```

**macOS/Linux:**
```bash
python3 build.py
```

The built executables will be in the `dist/` folder.

## 🔄 Updates

To update the Magic Wand:

1. **Pull the latest changes**
   ```bash
   git pull origin main
   ```

2. **Update dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Test the installation**
   ```bash
   python test_magic_wand.py
   ```

## 🆘 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Run the test suite** to identify problems
3. **Check the logs** for error messages
4. **Create an issue** on GitHub with details
5. **Join our Discord** for community support

---

**Happy coding with Magic Wand! ✨** 