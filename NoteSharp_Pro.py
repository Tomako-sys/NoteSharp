#!/usr/bin/env python3
"""
NoteSharp Pro - Enhanced Python Text Editor
A modern, feature-rich text editor with advanced capabilities
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from ui.themes import theme_manager
from ui.toolbar import ModernToolbar
from ui.sidebar import FileExplorer
from core.editor import EnhancedTextEditor
from features.terminal import IntegratedTerminal
from features.git_integration import GitIntegration

# Multi-language support (keeping the original LANG structure for compatibility)
LANG = {
    'en': {
        'file': "File",
        'new_tab': "New Tab",
        'open': "Open... (Ctrl+O)",
        'save': "Save (Ctrl+S)",
        'saveas': "Save As...",
        'close_tab': "Close Tab",
        'quit': "Quit (Ctrl+Q)",
        'recent': "Recent",
        'edit': "Edit",
        'undo': "Undo",
        'redo': "Redo",
        'cut': "Cut",
        'copy': "Copy",
        'paste': "Paste",
        'select_all': "Select All",
        'tools': "Tools",
        'find_replace': "Find/Replace... (Ctrl+F)",
        'goto_line': "Go to Line (Ctrl+G)",
        'view': "View",
        'theme': "Theme",
        'font': "Font...",
        'fontsize': "Font Size...",
        'language': "Language",
        'sidebar': "Toggle Sidebar",
        'terminal': "Toggle Terminal",
        'word_wrap': "Word Wrap",
        'line_numbers': "Line Numbers",
        'settings': "Settings",
        'about': "About",
        'zoom_in': "Zoom In",
        'zoom_out': "Zoom Out",
        'reset_zoom': "Reset Zoom",
        'tab_new': "New",
        'tab_locked': "🔒",
        'auto_save': "Auto Save",
        'read_only': "Read Only",
        'git': "Git",
        'plugins': "Plugins",
        'help': "Help"
    },
    'fr': {
        'file': "Fichier",
        'new_tab': "Nouvel onglet",
        'open': "Ouvrir... (Ctrl+O)",
        'save': "Enregistrer (Ctrl+S)",
        'saveas': "Enregistrer sous...",
        'close_tab': "Fermer l'onglet",
        'quit': "Quitter (Ctrl+Q)",
        'recent': "Récents",
        'edit': "Edition",
        'undo': "Annuler",
        'redo': "Refaire",
        'cut': "Couper",
        'copy': "Copier",
        'paste': "Coller",
        'select_all': "Sélectionner tout",
        'tools': "Outils",
        'find_replace': "Rechercher/remplacer... (Ctrl+F)",
        'goto_line': "Aller à la ligne (Ctrl+G)",
        'view': "Affichage",
        'theme': "Thème",
        'font': "Police...",
        'fontsize': "Taille de police...",
        'language': "Langue",
        'sidebar': "Basculer la barre latérale",
        'terminal': "Basculer le terminal",
        'word_wrap': "Retour à la ligne",
        'line_numbers': "Numéros de ligne",
        'settings': "Paramètres",
        'about': "À propos",
        'zoom_in': "Zoom avant",
        'zoom_out': "Zoom arrière",
        'reset_zoom': "Réinitialiser le zoom",
        'tab_new': "Nouveau",
        'tab_locked': "🔒",
        'auto_save': "Sauvegarde automatique",
        'read_only': "Lecture seule",
        'git': "Git",
        'plugins': "Plugins",
        'help': "Aide"
    }
}

class NoteSharpPro:
    """Main application class for NoteSharp Pro"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{Config.APP_NAME} v{Config.VERSION}")
        self.root.geometry(f"{Config.MIN_WINDOW_WIDTH}x{Config.MIN_WINDOW_HEIGHT}")
        self.root.minsize(800, 600)
        
        # Application state
        self.language = Config.DEFAULT_LANGUAGE
        self.tabs = []
        self.current_tab_index = 0
        self.recent_files = []
        
        # UI Components
        self.notebook = None
        self.toolbar = None
        self.sidebar = None
        self.terminal = None
        self.git_integration = None
        self.status_bar = None
        
        # Initialize the application
        self.setup_application()
        
        # Apply initial theme
        theme_manager.set_theme(Config.DEFAULT_THEME)
        
        # Create first tab
        self.add_new_tab()
        
        # Bind window events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_application(self):
        """Setup the main application interface"""
        # Create main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        # Create toolbar
        self.toolbar = ModernToolbar(main_container, self.get_toolbar_callbacks())
        
        # Create content area (sidebar + editor area)
        content_frame = tk.Frame(main_container)
        content_frame.pack(fill='both', expand=True)
        
        # Create sidebar
        self.sidebar = FileExplorer(content_frame, self.on_file_selected)
        
        # Create editor area
        editor_frame = tk.Frame(content_frame)
        editor_frame.pack(side='right', fill='both', expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(editor_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create terminal
        self.terminal = IntegratedTerminal(editor_frame)
        
        # Create git integration
        self.git_integration = GitIntegration(self.root, self.on_git_status_change)
        
        # Create menu bar
        self.create_menu_bar()
    
    def get_toolbar_callbacks(self):
        """Get callbacks for toolbar actions"""
        return {
            'new_file': self.add_new_tab,
            'open_file': self.open_file,
            'save_file': self.save_current_file,
            'undo': lambda: self.current_editor().text.event_generate('<<Undo>>'),
            'redo': lambda: self.current_editor().text.event_generate('<<Redo>>'),
            'cut': lambda: self.current_editor().text.event_generate('<<Cut>>'),
            'copy': lambda: self.current_editor().text.event_generate('<<Copy>>'),
            'paste': lambda: self.current_editor().text.event_generate('<<Paste>>'),
            'find': self.show_find_dialog,
            'replace': self.show_replace_dialog,
            'toggle_sidebar': self.toggle_sidebar,
            'toggle_terminal': self.toggle_terminal,
            'zoom_in': lambda: self.current_editor().zoom_in(),
            'zoom_out': lambda: self.current_editor().zoom_out(),
            'toggle_theme': self.cycle_theme,
            'settings': self.show_settings
        }
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        L = LANG[self.language]
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=L['new_tab'], command=self.add_new_tab, accelerator="Ctrl+T")
        file_menu.add_command(label=L['open'], command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label=L['save'], command=self.save_current_file, accelerator="Ctrl+S")
        file_menu.add_command(label=L['saveas'], command=self.save_current_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        
        # Recent files submenu
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label=L['recent'], menu=self.recent_menu)
        self.update_recent_menu()
        
        file_menu.add_separator()
        file_menu.add_command(label=L['close_tab'], command=self.close_current_tab, accelerator="Ctrl+W")
        file_menu.add_command(label=L['quit'], command=self.on_closing, accelerator="Ctrl+Q")
        menubar.add_cascade(label=L['file'], menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label=L['undo'], command=lambda: self.current_editor().text.event_generate('<<Undo>>'), accelerator="Ctrl+Z")
        edit_menu.add_command(label=L['redo'], command=lambda: self.current_editor().text.event_generate('<<Redo>>'), accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label=L['cut'], command=lambda: self.current_editor().text.event_generate('<<Cut>>'), accelerator="Ctrl+X")
        edit_menu.add_command(label=L['copy'], command=lambda: self.current_editor().text.event_generate('<<Copy>>'), accelerator="Ctrl+C")
        edit_menu.add_command(label=L['paste'], command=lambda: self.current_editor().text.event_generate('<<Paste>>'), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label=L['select_all'], command=lambda: self.current_editor().text.tag_add('sel', '1.0', 'end'), accelerator="Ctrl+A")
        menubar.add_cascade(label=L['edit'], menu=edit_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label=L['find_replace'], command=self.show_find_dialog, accelerator="Ctrl+F")
        tools_menu.add_command(label=L['goto_line'], command=lambda: self.current_editor().goto_line(), accelerator="Ctrl+G")
        tools_menu.add_separator()
        tools_menu.add_checkbutton(label=L['auto_save'], command=self.toggle_auto_save)
        tools_menu.add_checkbutton(label=L['read_only'], command=self.toggle_read_only)
        tools_menu.add_separator()
        tools_menu.add_command(label=L['git'], command=self.show_git_panel)
        menubar.add_cascade(label=L['tools'], menu=tools_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(label=L['sidebar'], command=self.toggle_sidebar, accelerator="Ctrl+B")
        view_menu.add_checkbutton(label=L['terminal'], command=self.toggle_terminal, accelerator="Ctrl+`")
        view_menu.add_separator()
        view_menu.add_checkbutton(label=L['word_wrap'], command=lambda: self.current_editor().toggle_word_wrap())
        view_menu.add_checkbutton(label=L['line_numbers'], command=lambda: self.current_editor().toggle_line_numbers())
        view_menu.add_separator()
        view_menu.add_command(label=L['zoom_in'], command=lambda: self.current_editor().zoom_in(), accelerator="Ctrl++")
        view_menu.add_command(label=L['zoom_out'], command=lambda: self.current_editor().zoom_out(), accelerator="Ctrl+-")
        view_menu.add_command(label=L['reset_zoom'], command=lambda: self.current_editor().reset_zoom(), accelerator="Ctrl+0")
        view_menu.add_separator()
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        for theme_name in Config.THEMES.keys():
            theme_menu.add_radiobutton(
                label=theme_name.title(),
                command=lambda t=theme_name: theme_manager.set_theme(t)
            )
        view_menu.add_cascade(label=L['theme'], menu=theme_menu)
        
        view_menu.add_command(label=L['font'], command=self.change_font)
        view_menu.add_command(label=L['fontsize'], command=self.change_font_size)
        menubar.add_cascade(label=L['view'], menu=view_menu)
        
        # Language menu
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_radiobutton(label="English", command=lambda: self.set_language('en'))
        lang_menu.add_radiobutton(label="Français", command=lambda: self.set_language('fr'))
        menubar.add_cascade(label=L['language'], menu=lang_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=L['about'], command=self.show_about)
        menubar.add_cascade(label=L['help'], menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        shortcuts = {
            '<Control-t>': self.add_new_tab,
            '<Control-o>': self.open_file,
            '<Control-s>': self.save_current_file,
            '<Control-Shift-s>': self.save_current_file_as,
            '<Control-w>': self.close_current_tab,
            '<Control-q>': self.on_closing,
            '<Control-f>': self.show_find_dialog,
            '<Control-h>': self.show_replace_dialog,
            '<Control-g>': lambda e: self.current_editor().goto_line(),
            '<Control-b>': lambda e: self.toggle_sidebar(),
            '<Control-grave>': lambda e: self.toggle_terminal(),
            '<F11>': self.toggle_fullscreen
        }
        
        for shortcut, callback in shortcuts.items():
            self.root.bind(shortcut, lambda e, cb=callback: cb())
    
    def add_new_tab(self):
        """Add a new editor tab"""
        # Create tab frame
        tab_frame = tk.Frame(self.notebook)
        
        # Create editor
        editor = EnhancedTextEditor(
            tab_frame,
            on_tab_title_change=lambda title: self.update_tab_title(tab_frame, title),
            on_file_change=self.on_file_changed
        )
        
        # Add tab to notebook
        tab_title = LANG[self.language]['tab_new']
        self.notebook.add(tab_frame, text=tab_title)
        self.tabs.append(editor)
        
        # Select the new tab
        self.notebook.select(len(self.tabs) - 1)
        self.current_tab_index = len(self.tabs) - 1
        
        # Focus on the editor
        editor.text.focus_set()
        
        return editor
    
    def close_current_tab(self):
        """Close the current tab"""
        if len(self.tabs) <= 1:
            messagebox.showinfo("Info", "Cannot close the last tab.")
            return
        
        current_editor = self.current_editor()
        
        # Check if tab is locked
        if current_editor.locked:
            messagebox.showwarning("Warning", "This tab is locked!")
            return
        
        # Ask to save changes
        if not current_editor.ask_save_changes():
            return
        
        # Remove tab
        current_index = self.notebook.index(self.notebook.select())
        self.notebook.forget(current_index)
        del self.tabs[current_index]
        
        # Update current tab index
        if current_index < len(self.tabs):
            self.current_tab_index = current_index
        else:
            self.current_tab_index = len(self.tabs) - 1
    
    def current_editor(self):
        """Get the current editor"""
        if self.tabs:
            current_index = self.notebook.index(self.notebook.select())
            return self.tabs[current_index]
        return None
    
    def update_tab_title(self, tab_frame, title):
        """Update tab title"""
        try:
            tab_index = None
            for i in range(self.notebook.index("end")):
                if self.notebook.nametowidget(self.notebook.tabs()[i]) == tab_frame:
                    tab_index = i
                    break
            
            if tab_index is not None:
                self.notebook.tab(tab_index, text=title)
        except Exception as e:
            print(f"Error updating tab title: {e}")
    
    def open_file(self):
        """Open a file"""
        editor = self.current_editor()
        if editor and editor.open_file():
            # Add to recent files
            if editor.file_path:
                self.add_to_recent_files(editor.file_path)
    
    def save_current_file(self):
        """Save the current file"""
        editor = self.current_editor()
        if editor:
            if editor.save_file():
                if editor.file_path:
                    self.add_to_recent_files(editor.file_path)
    
    def save_current_file_as(self):
        """Save the current file with a new name"""
        editor = self.current_editor()
        if editor:
            if editor.save_file_as():
                if editor.file_path:
                    self.add_to_recent_files(editor.file_path)
    
    def on_file_selected(self, file_path):
        """Handle file selection from sidebar"""
        editor = self.current_editor()
        if editor:
            if editor.open_file(file_path):
                self.add_to_recent_files(file_path)
    
    def on_file_changed(self, file_path, has_changes):
        """Handle file change notifications"""
        # Update git status if applicable
        if self.git_integration:
            self.git_integration.update_git_status()
    
    def add_to_recent_files(self, file_path):
        """Add file to recent files list"""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:Config.MAX_RECENT_FILES]
        self.update_recent_menu()
    
    def update_recent_menu(self):
        """Update recent files menu"""
        if not hasattr(self, 'recent_menu'):
            return
        
        self.recent_menu.delete(0, tk.END)
        
        for file_path in self.recent_files:
            filename = os.path.basename(file_path)
            self.recent_menu.add_command(
                label=f"{filename} - {file_path}",
                command=lambda fp=file_path: self.open_recent_file(fp)
            )
        
        if not self.recent_files:
            self.recent_menu.add_command(label="No recent files", state='disabled')
    
    def open_recent_file(self, file_path):
        """Open a recent file"""
        if os.path.exists(file_path):
            editor = self.current_editor()
            if editor:
                editor.open_file(file_path)
        else:
            messagebox.showerror("Error", f"File not found: {file_path}")
            self.recent_files.remove(file_path)
            self.update_recent_menu()
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        if self.sidebar:
            return self.sidebar.toggle_visibility()
    
    def toggle_terminal(self):
        """Toggle terminal visibility"""
        if self.terminal:
            return self.terminal.toggle_visibility()
    
    def toggle_auto_save(self):
        """Toggle auto-save for current editor"""
        editor = self.current_editor()
        if editor:
            if editor.auto_save_enabled:
                editor.disable_auto_save()
                messagebox.showinfo("Auto Save", "Auto save disabled")
            else:
                editor.enable_auto_save()
                messagebox.showinfo("Auto Save", "Auto save enabled")
    
    def toggle_read_only(self):
        """Toggle read-only mode for current editor"""
        editor = self.current_editor()
        if editor:
            editor.set_read_only(not editor.read_only)
            status = "enabled" if editor.read_only else "disabled"
            messagebox.showinfo("Read Only", f"Read-only mode {status}")
    
    def show_find_dialog(self):
        """Show find dialog"""
        # This would open a find/replace dialog
        # For now, using a simple dialog
        search_term = tk.simpledialog.askstring("Find", "Enter search term:")
        if search_term:
            editor = self.current_editor()
            if editor:
                pos = editor.find_text(search_term)
                if not pos:
                    messagebox.showinfo("Find", "Text not found")
    
    def show_replace_dialog(self):
        """Show replace dialog"""
        # Simple replace dialog
        old_text = tk.simpledialog.askstring("Replace", "Find:")
        if old_text:
            new_text = tk.simpledialog.askstring("Replace", "Replace with:")
            if new_text is not None:
                editor = self.current_editor()
                if editor:
                    count = editor.replace_text(old_text, new_text, all_occurrences=True)
                    messagebox.showinfo("Replace", f"Replaced {count} occurrences")
    
    def show_git_panel(self):
        """Show git integration panel"""
        if self.git_integration:
            # Create a popup window with git controls
            git_window = tk.Toplevel(self.root)
            git_window.title("Git Integration")
            git_window.geometry("400x300")
            git_window.transient(self.root)
            
            self.git_integration.create_git_panel(git_window)
    
    def on_git_status_change(self, git_status):
        """Handle git status changes"""
        # Update UI elements based on git status
        pass
    
    def cycle_theme(self):
        """Cycle through available themes"""
        themes = list(Config.THEMES.keys())
        current_theme = theme_manager.get_current_theme()
        current_index = themes.index(current_theme)
        next_index = (current_index + 1) % len(themes)
        theme_manager.set_theme(themes[next_index])
    
    def change_font(self):
        """Change font family"""
        from tkinter import font as tkfont
        families = list(tkfont.families())
        # Simple font selection - in a full implementation, you'd have a better dialog
        font_name = tk.simpledialog.askstring(
            "Font",
            "Enter font name:",
            initialvalue=Config.DEFAULT_FONT_FAMILY
        )
        if font_name and font_name in families:
            Config.DEFAULT_FONT_FAMILY = font_name
            # Apply to all editors
            for editor in self.tabs:
                editor.font_family = font_name
                editor.text.config(font=(font_name, editor.font_size + editor.zoom_level))
                if editor.show_line_numbers:
                    editor.line_numbers.config(font=(font_name, editor.font_size + editor.zoom_level))
    
    def change_font_size(self):
        """Change font size"""
        size = tk.simpledialog.askinteger(
            "Font Size",
            "Enter font size:",
            initialvalue=Config.DEFAULT_FONT_SIZE,
            minvalue=8,
            maxvalue=72
        )
        if size:
            Config.DEFAULT_FONT_SIZE = size
            # Apply to all editors
            for editor in self.tabs:
                editor.font_size = size
                editor.text.config(font=(editor.font_family, size + editor.zoom_level))
                if editor.show_line_numbers:
                    editor.line_numbers.config(font=(editor.font_family, size + editor.zoom_level))
    
    def set_language(self, language):
        """Set application language"""
        self.language = language
        # Rebuild menu bar with new language
        self.create_menu_bar()
    
    def show_settings(self):
        """Show settings dialog"""
        # Create settings window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Add settings controls here
        tk.Label(settings_window, text="Settings", font=('Arial', 16, 'bold')).pack(pady=10)
        tk.Label(settings_window, text="Settings panel - Coming soon!").pack(pady=20)
        
        close_btn = tk.Button(
            settings_window,
            text="Close",
            command=settings_window.destroy
        )
        close_btn.pack(pady=10)
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
{Config.APP_NAME} v{Config.VERSION}

A modern, feature-rich text editor with advanced capabilities.

Features:
• Multi-tab editing with syntax highlighting
• Integrated terminal and file explorer
• Git integration
• Auto-completion and code folding
• Multiple themes and customization options
• Multi-language support (English/French)

Built with Python and Tkinter
        """
        messagebox.showinfo("About NoteSharp Pro", about_text)
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def on_closing(self):
        """Handle application closing"""
        # Check for unsaved changes in all tabs
        for editor in self.tabs:
            if editor.text_changed:
                if not editor.ask_save_changes():
                    return
        
        # Save application state
        # In a full implementation, you'd save settings, recent files, etc.
        
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = NoteSharpPro()
        app.run()
    except Exception as e:
        print(f"Error starting NoteSharp Pro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()