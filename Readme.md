# ✨ Magic Wand AI Tool

A minimalist, hotkey-activated AI tool that transforms your text instantly. Replace the 10-step AI workflow with a 3-step "Magic Moment".

## 🚀 The Magic Moment

1. **Highlight Text**: Select any text anywhere on your screen
2. **Press Hotkey**: Press `Ctrl+Alt+A` to activate the Magic Wand
3. **Give Command**: Type your command and see the magic happen!

## 🎯 Perfect For

- **Developers**: Refactor code, add documentation, convert formats
- **Writers**: Improve text, translate, summarize
- **Students**: Explain concepts, format essays
- **Professionals**: Draft emails, format data

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Google AI Gemini API key

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd AI-assistant
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Your API Key

1. Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variable:

**Windows:**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**macOS/Linux:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

### Step 4: Run the Application

```bash
python magic_wand.py
```

## 🎮 Usage

1. **Start the app**: Run `python magic_wand.py`
2. **Select text**: Highlight any text in any application
3. **Activate**: Press `Ctrl+Alt+A`
4. **Command**: Type your transformation command
5. **Paste**: Press `Ctrl+V` to paste the transformed text

### Example Commands

- `"refactor this code"`
- `"add documentation"`
- `"translate to Spanish"`
- `"explain this"`
- `"make this more professional"`
- `"convert to JSON"`
- `"summarize this"`

## 🔧 Features

- **Global Hotkey**: Works in any application
- **Minimalist UI**: Clean, distraction-free interface
- **System Tray**: Runs quietly in the background
- **Instant Results**: No context switching required
- **Clipboard Integration**: Seamless copy/paste workflow

## 🛠️ Building Executables

### Windows (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico magic_wand.py
```

### macOS (.app)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.icns magic_wand.py
```

## 🎨 Customization

### Changing the Hotkey

Edit the hotkey in `magic_wand.py`:

```python
self.listener = keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+a': self.show_input_window  # Change this line
})
```

### Custom Prompts

Modify the prompt template in the `_process_command_async` method to customize AI behavior.

## 🐛 Troubleshooting

### Common Issues

1. **"API key not configured"**
   - Make sure you've set the `GEMINI_API_KEY` environment variable
   - Restart the application after setting the key

2. **Hotkey not working**
   - Ensure the application has permission to listen for global hotkeys
   - Try running as administrator on Windows

3. **System tray not showing**
   - Install `pystray` and `Pillow`: `pip install pystray Pillow`
   - Some Linux distributions may require additional packages

### Debug Mode

Run with verbose output:

```bash
python magic_wand.py --debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for modern UI
- Powered by [Google AI Gemini](https://ai.google.dev/)
- Inspired by the need for seamless AI integration

## 📞 Support

- Create an issue on GitHub
- Join our Discord community
- Email: support@magicwand.ai

---

**Made with ✨ by the Magic Wand team**

