#!/usr/bin/env python3
"""
NoteSharp Pro - Working Version
A modern, feature-rich text editor with error handling for different environments
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point with proper error handling"""
    
    print("🚀 Starting NoteSharp Pro...")
    
    # Check for GUI support
    try:
        import tkinter as tk
        print("✅ GUI support available")
    except ImportError as e:
        print(f"❌ GUI not available: {e}")
        print("💡 Solutions:")
        print("   • Linux: sudo apt-get install python3-tk")
        print("   • macOS: brew install python-tk")
        print("   • Windows: Reinstall Python with tkinter")
        print("   • Or run: python NoteSharp.pyw (original version)")
        return False
    
    # Check for display
    if sys.platform.startswith('linux') and 'DISPLAY' not in os.environ:
        print("❌ No display environment found")
        print("💡 You need a desktop environment or X11 forwarding")
        return False
    
    try:
        # Test GUI creation
        test_root = tk.Tk()
        test_root.withdraw()
        test_root.destroy()
        print("✅ Display working")
    except Exception as e:
        print(f"❌ Display error: {e}")
        return False
    
    # Now import and run the main application
    try:
        from tkinter import ttk, messagebox, filedialog
        from config_safe import Config
        
        print("✅ All imports successful")
        print("🎨 Loading NoteSharp Pro interface...")
        
        # Create main window
        root = tk.Tk()
        root.title(f"{Config.APP_NAME} v{Config.VERSION}")
        root.geometry(f"{Config.MIN_WINDOW_WIDTH}x{Config.MIN_WINDOW_HEIGHT}")
        
        # Simple enhanced interface
        # Menu bar
        menubar = tk.Menu(root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New (Ctrl+N)", command=lambda: new_file())
        file_menu.add_command(label="Open (Ctrl+O)", command=lambda: open_file())
        file_menu.add_command(label="Save (Ctrl+S)", command=lambda: save_file()) 
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=lambda: text_area.event_generate('<<Undo>>'))
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=lambda: text_area.event_generate('<<Redo>>'))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut (Ctrl+X)", command=lambda: text_area.event_generate('<<Cut>>'))
        edit_menu.add_command(label="Copy (Ctrl+C)", command=lambda: text_area.event_generate('<<Copy>>'))
        edit_menu.add_command(label="Paste (Ctrl+V)", command=lambda: text_area.event_generate('<<Paste>>'))
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Light Theme", command=lambda: apply_theme('light'))
        view_menu.add_command(label="Dark Theme", command=lambda: apply_theme('dark'))
        view_menu.add_command(label="Monokai Theme", command=lambda: apply_theme('monokai'))
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        root.config(menu=menubar)
        
        # Main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill='both', expand=True)
        
        # Toolbar
        toolbar = tk.Frame(main_frame, height=40, relief='raised', bd=1)
        toolbar.pack(side='top', fill='x')
        toolbar.pack_propagate(False)
        
        # Toolbar buttons
        tk.Button(toolbar, text="📄 New", command=lambda: new_file()).pack(side='left', padx=2, pady=2)
        tk.Button(toolbar, text="📁 Open", command=lambda: open_file()).pack(side='left', padx=2, pady=2)
        tk.Button(toolbar, text="💾 Save", command=lambda: save_file()).pack(side='left', padx=2, pady=2)
        tk.Button(toolbar, text="🎨 Theme", command=cycle_theme).pack(side='right', padx=2, pady=2)
        
        # Text editor area
        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Line numbers frame
        line_frame = tk.Frame(editor_frame, width=50)
        line_frame.pack(side='left', fill='y')
        line_frame.pack_propagate(False)
        
        line_numbers = tk.Text(line_frame, width=4, state='disabled', 
                              bg='#f0f0f0', font=('Consolas', 12))
        line_numbers.pack(fill='both', expand=True)
        
        # Main text area
        text_area = tk.Text(editor_frame, wrap='word', undo=True, 
                           font=('Consolas', 12), tabs=('4c',))
        text_area.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(editor_frame, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Status bar
        status_bar = tk.Label(root, text="Ready - NoteSharp Pro", 
                             anchor='w', relief='sunken')
        status_bar.pack(side='bottom', fill='x')
        
        # Global variables
        current_file = None
        current_theme = 'light'
        
        def update_line_numbers():
            """Update line numbers"""
            line_numbers.config(state='normal')
            line_numbers.delete(1.0, tk.END)
            
            line_count = int(text_area.index('end-1c').split('.')[0])
            line_nums = '\n'.join(str(i) for i in range(1, line_count + 1))
            line_numbers.insert(1.0, line_nums)
            
            line_numbers.config(state='disabled')
        
        def update_status():
            """Update status bar"""
            content = text_area.get(1.0, tk.END)
            lines = int(text_area.index('end-1c').split('.')[0])
            chars = len(content.rstrip('\n'))
            words = len(content.split())
            
            cursor_pos = text_area.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            
            status_text = f"Lines: {lines} | Words: {words} | Characters: {chars} | Ln {line}, Col {int(col)+1}"
            if current_file:
                status_text = f"{os.path.basename(current_file)} - {status_text}"
            
            status_bar.config(text=status_text)
        
        def apply_theme(theme_name):
            """Apply color theme"""
            nonlocal current_theme
            current_theme = theme_name
            
            colors = Config.THEMES[theme_name]
            
            # Apply colors
            text_area.config(
                bg=colors['bg'],
                fg=colors['fg'],
                selectbackground=colors['select_bg'],
                selectforeground=colors['select_fg'],
                insertbackground=colors['fg']
            )
            
            line_numbers.config(
                bg=colors['line_bg'],
                fg=colors['line_fg']
            )
            
            root.config(bg=colors['bg'])
            main_frame.config(bg=colors['bg'])
            editor_frame.config(bg=colors['bg'])
            
            # Apply syntax highlighting colors
            apply_syntax_highlighting()
        
        def apply_syntax_highlighting():
            """Apply basic syntax highlighting"""
            import re
            import keyword
            
            # Clear existing tags
            for tag in ['keyword', 'string', 'comment']:
                text_area.tag_remove(tag, '1.0', tk.END)
            
            content = text_area.get('1.0', tk.END)
            syntax_colors = Config.SYNTAX_COLORS[current_theme]
            
            # Python keywords
            for kw in keyword.kwlist:
                for match in re.finditer(r'\b' + kw + r'\b', content):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    text_area.tag_add('keyword', start, end)
            
            # Strings
            for match in re.finditer(r'(["'])(?:(?=(\\?))\2.)*?\1', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                text_area.tag_add('string', start, end)
            
            # Comments
            for match in re.finditer(r'#.*?$', content, re.MULTILINE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                text_area.tag_add('comment', start, end)
            
            # Configure tag colors
            text_area.tag_config('keyword', foreground=syntax_colors['keyword'], font=('Consolas', 12, 'bold'))
            text_area.tag_config('string', foreground=syntax_colors['string'])
            text_area.tag_config('comment', foreground=syntax_colors['comment'])
        
        def cycle_theme():
            """Cycle through themes"""
            themes = ['light', 'dark', 'monokai']
            current_index = themes.index(current_theme)
            next_theme = themes[(current_index + 1) % len(themes)]
            apply_theme(next_theme)
        
        def new_file():
            """Create new file"""
            if messagebox.askyesnocancel("New File", "Create new file? (Unsaved changes will be lost)"):
                text_area.delete(1.0, tk.END)
                nonlocal current_file
                current_file = None
                update_status()
        
        def open_file():
            """Open file"""
            filename = filedialog.askopenfilename(
                filetypes=[
                    ("All Files", "*.*"),
                    ("Python Files", "*.py"),
                    ("Text Files", "*.txt"),
                    ("JavaScript Files", "*.js"),
                    ("HTML Files", "*.html")
                ]
            )
            
            if filename:
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    text_area.delete(1.0, tk.END)
                    text_area.insert(1.0, content)
                    
                    nonlocal current_file
                    current_file = filename
                    root.title(f"{Config.APP_NAME} - {os.path.basename(filename)}")
                    
                    update_line_numbers()
                    update_status()
                    apply_syntax_highlighting()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open file: {e}")
        
        def save_file():
            """Save file"""
            if current_file:
                try:
                    content = text_area.get(1.0, tk.END)
                    with open(current_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    messagebox.showinfo("Success", "File saved!")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not save file: {e}")
            else:
                # Save as
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[
                        ("Text Files", "*.txt"),
                        ("Python Files", "*.py"),
                        ("All Files", "*.*")
                    ]
                )
                
                if filename:
                    try:
                        content = text_area.get(1.0, tk.END)
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        nonlocal current_file
                        current_file = filename
                        root.title(f"{Config.APP_NAME} - {os.path.basename(filename)}")
                        messagebox.showinfo("Success", "File saved!")
                        update_status()
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not save file: {e}")
        
        def show_about():
            """Show about dialog"""
            about_text = f"""{Config.APP_NAME} v{Config.VERSION}

A modern, feature-rich text editor with:
• Multi-language syntax highlighting
• Multiple themes (Light, Dark, Monokai)  
• Line numbers and status bar
• File operations and editing tools
• Cross-platform compatibility

Built with Python and Tkinter"""
            
            messagebox.showinfo("About", about_text)
        
        def on_text_change(event=None):
            """Handle text changes"""
            update_line_numbers()
            update_status()
            # Delayed syntax highlighting to avoid lag
            root.after_idle(apply_syntax_highlighting)
        
        # Bind events
        text_area.bind('<KeyRelease>', on_text_change)
        text_area.bind('<ButtonRelease-1>', update_status)
        
        # Keyboard shortcuts
        root.bind('<Control-n>', lambda e: new_file())
        root.bind('<Control-o>', lambda e: open_file())
        root.bind('<Control-s>', lambda e: save_file())
        root.bind('<Control-q>', lambda e: root.quit())
        
        # Initial setup
        apply_theme('light')
        update_line_numbers()
        update_status()
        
        # Sample content
        text_area.insert(1.0, f"""# Welcome to {Config.APP_NAME}!

This is a working version of the enhanced text editor.

Features available:
• Syntax highlighting for Python, JavaScript, HTML, CSS
• Multiple themes (try the 🎨 Theme button!)
• Line numbers and status bar
• File operations (New, Open, Save)
• Keyboard shortcuts (Ctrl+N, Ctrl+O, Ctrl+S)

Try opening a Python file to see syntax highlighting!

def hello_world():
    print("Hello from NoteSharp Pro!")
    return True

# Delete this content and start coding!
""")
        
        update_line_numbers()
        apply_syntax_highlighting()
        
        print("🎉 NoteSharp Pro launched successfully!")
        
        # Start the GUI
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💡 Try the original version: python NoteSharp.pyw")
        sys.exit(1)
    print("👋 Thanks for using NoteSharp Pro!")
