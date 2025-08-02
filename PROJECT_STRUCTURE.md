# 📁 Magic Wand AI Tool - Project Structure

This document provides an overview of all files in the Magic Wand AI Tool project.

## 🎯 Core Application Files

### `magic_wand.py`
- **Purpose**: Main application file
- **Description**: Contains the MagicWandApp class with global hotkey listener, GUI, and AI integration
- **Key Features**: 
  - Global hotkey detection (`Ctrl+Alt+A`)
  - Minimalist GUI with customtkinter
  - Clipboard integration
  - Google AI Gemini API integration
  - System tray support

### `config.py`
- **Purpose**: Configuration management
- **Description**: Centralized configuration for all application settings
- **Key Features**:
  - Hotkey customization
  - UI theme settings
  - API model selection
  - Window dimensions
  - Status messages
  - Validation functions

## 📦 Dependencies & Setup

### `requirements.txt`
- **Purpose**: Python dependencies list
- **Description**: Lists all required packages with specific versions
- **Dependencies**:
  - `customtkinter==5.2.2` - Modern GUI framework
  - `pyperclip==1.8.2` - Clipboard management
  - `pynput==1.7.6` - Global hotkey detection
  - `google-generativeai==0.8.3` - Google AI API
  - `pystray==0.19.5` - System tray icon
  - `Pillow==10.2.0` - Image processing

### `setup.py`
- **Purpose**: Automated installation script
- **Description**: Handles dependency installation, API key setup, and startup script creation
- **Features**:
  - Python version checking
  - Dependency installation
  - API key configuration
  - Platform-specific startup scripts
  - Environment variable setup

## 🛠️ Build & Distribution

### `build.py`
- **Purpose**: Executable building script
- **Description**: Creates standalone executables for Windows, macOS, and Linux
- **Features**:
  - PyInstaller integration
  - Platform-specific builds
  - Installer script generation
  - Clean build directories

### `magic_wand.spec`
- **Purpose**: PyInstaller specification file
- **Description**: Configuration for building Windows executable
- **Features**:
  - Hidden imports configuration
  - Executable settings
  - Icon and metadata

## 🧪 Testing & Demo

### `test_magic_wand.py`
- **Purpose**: Comprehensive test suite
- **Description**: Tests all core functionality without running the full application
- **Test Categories**:
  - Configuration validation
  - API connection testing
  - Dependency checking
  - Clipboard functionality
  - Hotkey configuration

### `demo.py`
- **Purpose**: Functionality demonstration
- **Description**: Shows sample text transformations using the AI
- **Features**:
  - Sample text transformations
  - Usage workflow demonstration
  - Configuration display
  - Example commands

## 📚 Documentation

### `README.md`
- **Purpose**: Main project documentation
- **Description**: Comprehensive guide with installation, usage, and troubleshooting
- **Sections**:
  - Project overview
  - Installation instructions
  - Usage guide
  - Feature list
  - Troubleshooting
  - Contributing guidelines

### `INSTALL.md`
- **Purpose**: Detailed installation guide
- **Description**: Step-by-step installation for Windows, macOS, and Linux
- **Features**:
  - Multiple installation methods
  - Platform-specific instructions
  - Troubleshooting section
  - Configuration guide

### `PROJECT_STRUCTURE.md`
- **Purpose**: This file - project overview
- **Description**: Lists all files and their purposes

## 🚀 Startup Scripts

### `start_magic_wand.py`
- **Purpose**: Enhanced startup script
- **Description**: Loads environment variables and starts the application
- **Features**:
  - .env file support
  - Environment variable loading
  - Error handling

### `start_magic_wand.bat` (Windows)
- **Purpose**: Windows batch file
- **Description**: Easy-to-use startup script for Windows users

### `start_magic_wand.command` (macOS)
- **Purpose**: macOS shell script
- **Description**: Easy-to-use startup script for macOS users

## 📋 Installation Scripts

### `install.bat` (Windows)
- **Purpose**: Windows installer
- **Description**: Copies executable to desktop for easy access

### `install.command` (macOS)
- **Purpose**: macOS installer
- **Description**: Copies application to Applications folder

## 🔧 Configuration Files

### `.env` (Generated)
- **Purpose**: Environment variables storage
- **Description**: Stores API key and other environment variables
- **Note**: Created by setup.py, not included in repository

## 📦 Build Output

### `dist/` (Generated)
- **Purpose**: Build output directory
- **Contents**:
  - `MagicWand.exe` (Windows executable)
  - `MagicWand` (macOS/Linux executable)

### `build/` (Generated)
- **Purpose**: PyInstaller build files
- **Note**: Temporary build directory

## 🎯 File Relationships

```
magic_wand.py (Main App)
    ↓
config.py (Configuration)
    ↓
requirements.txt (Dependencies)
    ↓
setup.py (Installation)
    ↓
build.py (Build Process)
    ↓
magic_wand.spec (Build Config)
    ↓
dist/MagicWand.exe (Final Executable)
```

## 🚀 Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set API key**: `set GEMINI_API_KEY=your_key` (Windows) or `export GEMINI_API_KEY=your_key` (macOS/Linux)
3. **Test installation**: `python test_magic_wand.py`
4. **Run application**: `python magic_wand.py`
5. **Use hotkey**: Press `Ctrl+Alt+A` to activate

## 🔧 Customization

- **Hotkey**: Edit `HOTKEY` in `config.py`
- **UI Theme**: Edit `UI_THEME` in `config.py`
- **AI Model**: Edit `AI_MODEL` in `config.py`
- **Window Size**: Edit `WINDOW_WIDTH` and `WINDOW_HEIGHT` in `config.py`

## 🧪 Testing

- **Full test suite**: `python test_magic_wand.py`
- **Quick test**: `python test_magic_wand.py --quick`
- **Demo mode**: `python demo.py`

## 🛠️ Building

- **Windows**: `python build.py`
- **macOS**: `python3 build.py`
- **Linux**: `python3 build.py`

---

**Total Files**: 15+ files (including generated files)
**Lines of Code**: ~2000+ lines
**Supported Platforms**: Windows, macOS, Linux
**License**: MIT 