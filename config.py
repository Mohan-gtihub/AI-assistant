"""
Configuration file for Magic Wand AI Tool
Modify these settings to customize the application
"""

import os

# ============================================================================
# HOTKEY CONFIGURATION
# ============================================================================

# Global hotkey to activate the Magic Wand
# Format: '<ctrl>+<alt>+key' or '<ctrl>+<shift>+key'
HOTKEY = '<ctrl>+<alt>+a'

# Alternative hotkeys you can use:
# '<ctrl>+<alt>+w'  # Magic Wand
# '<ctrl>+<alt>+m'  # Magic
# '<ctrl>+<alt>+t'  # Transform
# '<ctrl>+<shift>+a'  # Alternative combination

# ============================================================================
# UI CONFIGURATION
# ============================================================================

# Window appearance
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 150
WINDOW_TITLE = "Magic Wand"

# UI Theme
UI_THEME = "dark"  # Options: "dark", "light", "system"
UI_COLOR_THEME = "blue"  # Options: "blue", "green", "dark-blue"

# Placeholder text for the input field
INPUT_PLACEHOLDER = "Enter your command (e.g., 'refactor this', 'explain this', 'translate to Spanish')"

# Status messages
STATUS_READY = "Ready to transform your text!"
STATUS_PROCESSING = "Processing..."
STATUS_SUCCESS = "Text transformed! Press Ctrl+V to paste."
STATUS_ERROR = "Error: API key not configured"

# ============================================================================
# AI CONFIGURATION
# ============================================================================

# Google AI Gemini model to use
# Options: "gemini-flash-exp", "gemini-pro", "gemini-1.5-flash"
AI_MODEL = "gemini-flash-exp"

# API key environment variable name
API_KEY_ENV = "GEMINI_API_KEY"

# Prompt template for AI requests
PROMPT_TEMPLATE = """
You are a helpful AI assistant. The user has selected some text and wants you to transform it based on their command.

User's command: {command}

Selected text:
{text}

Please transform the text according to the user's command. Return ONLY the transformed text, nothing else.
"""

# ============================================================================
# SYSTEM TRAY CONFIGURATION
# ============================================================================

# System tray icon settings
SYSTEM_TRAY_ENABLED = True
SYSTEM_TRAY_ICON_SIZE = 64
SYSTEM_TRAY_MENU_ITEMS = [
    "Show Magic Wand",
    "Exit"
]

# ============================================================================
# BEHAVIOR CONFIGURATION
# ============================================================================

# Auto-hide window after successful transformation (seconds)
AUTO_HIDE_DELAY = 2.0

# Enable debug mode
DEBUG_MODE = False

# Enable verbose logging
VERBOSE_LOGGING = False

# ============================================================================
# ADVANCED CONFIGURATION
# ============================================================================

# Threading settings
MAX_WORKER_THREADS = 2

# API timeout settings (seconds)
API_TIMEOUT = 30

# Clipboard settings
CLIPBOARD_TIMEOUT = 5

# ============================================================================
# ENVIRONMENT DETECTION
# ============================================================================

def get_api_key():
    """Get API key from environment variable"""
    return os.getenv(API_KEY_ENV)

def is_windows():
    """Check if running on Windows"""
    import platform
    return platform.system() == "Windows"

def is_macos():
    """Check if running on macOS"""
    import platform
    return platform.system() == "Darwin"

def is_linux():
    """Check if running on Linux"""
    import platform
    return platform.system() == "Linux"

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check API key
    if not get_api_key():
        errors.append(f"API key not found. Please set the {API_KEY_ENV} environment variable.")
    
    # Check hotkey format
    if not HOTKEY or '+' not in HOTKEY:
        errors.append("Invalid hotkey format. Use format like '<ctrl>+<alt>+a'")
    
    # Check window dimensions
    if WINDOW_WIDTH < 200 or WINDOW_HEIGHT < 100:
        errors.append("Window dimensions too small. Minimum: 200x100")
    
    return errors

# ============================================================================
# CONFIGURATION HELPERS
# ============================================================================

def get_config_summary():
    """Get a summary of current configuration"""
    return {
        "hotkey": HOTKEY,
        "model": AI_MODEL,
        "theme": UI_THEME,
        "window_size": f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}",
        "api_key_configured": bool(get_api_key()),
        "system_tray_enabled": SYSTEM_TRAY_ENABLED,
        "auto_hide_delay": AUTO_HIDE_DELAY,
        "debug_mode": DEBUG_MODE
    }

def print_config_summary():
    """Print current configuration summary"""
    print("🔧 Magic Wand Configuration:")
    print("=" * 40)
    
    config = get_config_summary()
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Check for errors
    errors = validate_config()
    if errors:
        print("\n⚠️  Configuration Issues:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ Configuration is valid!") 