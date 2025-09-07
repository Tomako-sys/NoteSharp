# Modern toolbar for NoteSharp
import tkinter as tk
from tkinter import ttk
from ui.themes import theme_manager
from config import Config

class ModernToolbar:
    """Modern toolbar with icons and improved styling"""
    
    def __init__(self, parent, callbacks=None):
        self.parent = parent
        self.callbacks = callbacks or {}
        self.toolbar_frame = None
        self.buttons = {}
        self.create_toolbar()
        
        # Register for theme changes
        theme_manager.add_observer(self.on_theme_change)
    
    def create_toolbar(self):
        """Create the toolbar with all buttons"""
        if self.toolbar_frame:
            self.toolbar_frame.destroy()
        
        colors = theme_manager.get_colors()
        self.toolbar_frame = tk.Frame(self.parent, bg=colors['toolbar_bg'], height=35)
        self.toolbar_frame.pack(fill='x', padx=2, pady=2)
        self.toolbar_frame.pack_propagate(False)
        
        # File operations
        file_frame = tk.Frame(self.toolbar_frame, bg=colors['toolbar_bg'])
        file_frame.pack(side='left', padx=5)
        
        self.create_button(file_frame, "New", "📄", "new_file")
        self.create_button(file_frame, "Open", "📁", "open_file")
        self.create_button(file_frame, "Save", "💾", "save_file")
        
        # Separator
        separator1 = tk.Frame(self.toolbar_frame, width=2, bg=colors['border'])
        separator1.pack(side='left', fill='y', padx=5)
        
        # Edit operations
        edit_frame = tk.Frame(self.toolbar_frame, bg=colors['toolbar_bg'])
        edit_frame.pack(side='left', padx=5)
        
        self.create_button(edit_frame, "Undo", "↶", "undo")
        self.create_button(edit_frame, "Redo", "↷", "redo")
        self.create_button(edit_frame, "Cut", "✂️", "cut")
        self.create_button(edit_frame, "Copy", "📋", "copy")
        self.create_button(edit_frame, "Paste", "📌", "paste")
        
        # Separator
        separator2 = tk.Frame(self.toolbar_frame, width=2, bg=colors['border'])
        separator2.pack(side='left', fill='y', padx=5)
        
        # Search operations
        search_frame = tk.Frame(self.toolbar_frame, bg=colors['toolbar_bg'])
        search_frame.pack(side='left', padx=5)
        
        self.create_button(search_frame, "Find", "🔍", "find")
        self.create_button(search_frame, "Replace", "🔄", "replace")
        
        # Separator
        separator3 = tk.Frame(self.toolbar_frame, width=2, bg=colors['border'])
        separator3.pack(side='left', fill='y', padx=5)
        
        # View operations
        view_frame = tk.Frame(self.toolbar_frame, bg=colors['toolbar_bg'])
        view_frame.pack(side='left', padx=5)
        
        self.create_button(view_frame, "Sidebar", "📂", "toggle_sidebar")
        self.create_button(view_frame, "Terminal", "⚡", "toggle_terminal")
        self.create_button(view_frame, "Zoom In", "🔍+", "zoom_in")
        self.create_button(view_frame, "Zoom Out", "🔍-", "zoom_out")
        
        # Right side - Theme and settings
        right_frame = tk.Frame(self.toolbar_frame, bg=colors['toolbar_bg'])
        right_frame.pack(side='right', padx=5)
        
        self.create_button(right_frame, "Theme", "🎨", "toggle_theme")
        self.create_button(right_frame, "Settings", "⚙️", "settings")
    
    def create_button(self, parent, text, icon, action):
        """Create a toolbar button with icon and text"""
        colors = theme_manager.get_colors()
        
        button = tk.Button(
            parent,
            text=f"{icon}",
            bg=colors['button_bg'],
            fg=colors['fg'],
            activebackground=colors['button_hover'],
            activeforeground=colors['fg'],
            relief='flat',
            bd=0,
            padx=6,
            pady=4,
            font=('Segoe UI Emoji', 10),
            cursor='hand2',
            command=lambda: self.execute_action(action)
        )
        button.pack(side='left', padx=1)
        
        # Add hover effects
        def on_enter(e):
            button.config(bg=colors['button_hover'])
        
        def on_leave(e):
            button.config(bg=colors['button_bg'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        # Tooltip
        self.create_tooltip(button, text)
        
        self.buttons[action] = button
        return button
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            colors = theme_manager.get_colors()
            label = tk.Label(
                tooltip,
                text=text,
                bg=colors['status_bg'],
                fg=colors['status_fg'],
                relief='solid',
                bd=1,
                font=('Segoe UI', 9),
                padx=4,
                pady=2
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def execute_action(self, action):
        """Execute a toolbar action"""
        if action in self.callbacks:
            try:
                self.callbacks[action]()
            except Exception as e:
                print(f"Error executing toolbar action {action}: {e}")
    
    def on_theme_change(self, theme_name):
        """Handle theme change"""
        self.create_toolbar()
    
    def set_callback(self, action, callback):
        """Set a callback for a toolbar action"""
        self.callbacks[action] = callback
    
    def get_frame(self):
        """Get the toolbar frame"""
        return self.toolbar_frame