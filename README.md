# NoteSharp Pro

A modern, feature-rich text editor with advanced capabilities - Enhanced version with powerful productivity tools, integrated terminal, git support, and much more!

Built with Python + Tkinter with a completely redesigned architecture for extensibility and performance.

---

## 🚀 Enhanced Features

### 📝 **Advanced Text Editing**
- **Multi-Tab Editing:** Work with multiple files simultaneously with enhanced tab management
- **Advanced Syntax Highlighting:** Support for Python, JavaScript, HTML, CSS, JSON, C/C++, Java, PHP, Ruby, Go, Rust, SQL, and more
- **Auto-Completion:** Intelligent code completion with language-specific suggestions and snippets
- **Code Folding:** Collapse and expand code blocks for better navigation
- **Line Numbers:** Enhanced line numbering with click-to-go functionality
- **Advanced Find & Replace:** Powerful search and replace with regex support
- **Multiple Cursors:** Edit multiple locations simultaneously (Coming soon)

### 🎨 **Modern UI & Themes**
- **Multiple Themes:** Light, Dark, and Monokai themes with customizable color schemes
- **Modern Toolbar:** Icon-based toolbar with tooltips and hover effects
- **Responsive Design:** Adaptive UI that works well on different screen sizes
- **Font Customization:** Change font family and size with zoom in/out support
- **Status Bar:** Rich status information including cursor position, encoding, language, and statistics

### 📁 **File Management**
- **File Explorer Sidebar:** Navigate your project files with a built-in file tree
- **Recent Files:** Enhanced recent files menu with quick access
- **Project Support:** Work with multiple files and folders efficiently
- **Auto-Save:** Configurable auto-save with customizable intervals
- **Large File Support:** Handle large files with performance optimizations

### ⚡ **Integrated Terminal**
- **Built-in Terminal:** Full terminal integration with command history
- **Directory Navigation:** Navigate directories directly from the terminal
- **Command Auto-completion:** Basic auto-completion for files and directories
- **Process Management:** Run and manage processes from within the editor

### 🔄 **Git Integration**
- **Git Status:** Real-time git status display
- **Basic Git Operations:** Add, commit, push, pull directly from the editor
- **Branch Information:** Current branch display and management
- **File Status Indicators:** Visual indicators for modified, added, and untracked files

### ⌨️ **Advanced Keyboard Support**
- **Extensive Shortcuts:** Comprehensive keyboard shortcuts for all operations
- **Custom Key Bindings:** Customizable keyboard shortcuts (Coming soon)
- **Vim Keybindings:** Optional Vim key bindings (Coming soon)
- **Multi-platform Support:** Works consistently across Windows, macOS, and Linux

### 🛠️ **Developer Tools**
- **Comment Toggle:** Smart comment/uncomment for all supported languages
- **Line Manipulation:** Move lines up/down, duplicate lines, join lines
- **Text Transformation:** UPPERCASE/lowercase conversion, smart indentation
- **Bracket Matching:** Automatic bracket matching and highlighting
- **Smart Indentation:** Language-aware indentation

### 🌍 **Internationalization**
- **Multi-language Support:** Full English and French interface support
- **Extensible Localization:** Easy to add more languages

### 🔧 **Extensibility & Configuration**
- **Plugin System:** Foundation for plugin development (Coming soon)
- **Configuration Management:** Centralized configuration system
- **Theme Customization:** Create and modify themes
- **Modular Architecture:** Clean, extensible codebase

---

## 📦 Installation & Requirements

**Requirements:**  
- Python 3.8+ (with tkinter - included in standard Python distributions)
- No external dependencies required!

**Installation:**
```bash
# Clone or download the repository
git clone <repository-url>
cd notesharp-pro

# Run the application
python NoteSharp_Pro.py
```

**Alternative (Original Version):**
```bash
# Run the original version
python NoteSharp.pyw
```

---

## 🚀 Quick Start

1. **Launch NoteSharp Pro:** Run `python NoteSharp_Pro.py`
2. **Create or Open Files:** Use Ctrl+T for new tab, Ctrl+O to open files
3. **Explore the Sidebar:** Toggle with Ctrl+B to browse your project files
4. **Use the Terminal:** Toggle with Ctrl+` for integrated terminal access
5. **Try Different Themes:** Use the theme button in toolbar or View menu
6. **Customize Settings:** Access settings from toolbar or Tools menu

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | New Tab |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save File |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+W` | Close Tab |
| `Ctrl+F` | Find |
| `Ctrl+H` | Replace |
| `Ctrl+G` | Go to Line |
| `Ctrl+B` | Toggle Sidebar |
| `Ctrl+`\` ` | Toggle Terminal |
| `Ctrl+D` | Duplicate Line |
| `Ctrl+/` | Toggle Comment |
| `Ctrl+Plus` | Zoom In |
| `Ctrl+Minus` | Zoom Out |
| `Ctrl+0` | Reset Zoom |
| `Alt+Up/Down` | Move Line Up/Down |
| `F11` | Toggle Fullscreen |

---

## 🎨 Themes

NoteSharp Pro comes with three built-in themes:

- **Light Theme:** Classic light theme with high contrast
- **Dark Theme:** Modern dark theme easy on the eyes
- **Monokai:** Popular programming theme with vibrant colors

Themes can be switched from the toolbar, View menu, or by cycling with the theme button.

---

## 📁 Project Structure

```
/app/
├── NoteSharp_Pro.py          # Main enhanced application
├── NoteSharp.pyw            # Original version (still included)
├── config.py                # Global configuration
├── ui/                      # UI components
│   ├── themes.py           # Theme management
│   ├── toolbar.py          # Modern toolbar
│   └── sidebar.py          # File explorer
├── core/                    # Core functionality
│   └── editor.py           # Enhanced text editor
├── syntax/                  # Syntax highlighting
│   ├── highlighter.py      # Multi-language highlighter
│   └── autocomplete.py     # Auto-completion system
├── features/               # Advanced features
│   ├── terminal.py         # Integrated terminal
│   └── git_integration.py  # Git support
└── README.md               # This file
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues:** Found a bug? Report it in the issues section
2. **Feature Requests:** Have an idea? Let us know!
3. **Code Contributions:** Fork, improve, and submit pull requests
4. **Documentation:** Help improve documentation and examples
5. **Themes:** Create and share new themes
6. **Language Support:** Add syntax highlighting for new languages

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute according to the license terms.

---

## 🎯 Roadmap

### 🔜 Coming Soon
- [ ] Plugin system with API
- [ ] Multiple cursor support
- [ ] Vim key bindings
- [ ] Split view editing
- [ ] Advanced search (regex, in files)
- [ ] Code formatting integration
- [ ] Debugger integration
- [ ] More programming languages
- [ ] Remote file editing (SSH/FTP)
- [ ] Collaborative editing

### 💡 Future Ideas
- [ ] AI-powered code completion
- [ ] Live collaboration
- [ ] Code snippets manager
- [ ] Integrated task runner
- [ ] Database query tools
- [ ] Markdown preview
- [ ] PDF export
- [ ] Mobile companion app

---

## 📞 Support

- **Documentation:** Check the built-in help system
- **Issues:** Report bugs and request features on GitHub
- **Community:** Join our community discussions
- **Email:** Contact the developers directly

---

**NoteSharp Pro** - Elevating your text editing experience! 🚀
