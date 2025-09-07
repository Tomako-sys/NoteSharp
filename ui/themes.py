# Theme management for NoteSharp
import tkinter as tk
from tkinter import ttk
from config import Config

class ThemeManager:
    """Manages themes and styling for the application"""
    
    def __init__(self):
        self.current_theme = Config.DEFAULT_THEME
        self.observers = []
    
    def add_observer(self, callback):
        """Add a callback to be notified when theme changes"""
        self.observers.append(callback)
    
    def remove_observer(self, callback):
        """Remove a callback from theme change notifications"""
        if callback in self.observers:
            self.observers.remove(callback)
    
    def set_theme(self, theme_name):
        """Change the current theme"""
        if theme_name in Config.THEMES:
            self.current_theme = theme_name
            self._notify_observers()
    
    def get_current_theme(self):
        """Get the current theme name"""
        return self.current_theme
    
    def get_colors(self):
        """Get colors for the current theme"""
        return Config.THEMES[self.current_theme]
    
    def get_syntax_colors(self):
        """Get syntax highlighting colors for the current theme"""
        return Config.SYNTAX_COLORS[self.current_theme]
    
    def _notify_observers(self):
        """Notify all observers of theme change"""
        for callback in self.observers:
            try:
                callback(self.current_theme)
            except Exception as e:
                print(f"Error notifying theme observer: {e}")
    
    def apply_theme_to_widget(self, widget, widget_type='text'):
        """Apply current theme to a widget"""
        colors = self.get_colors()
        
        try:
            if widget_type == 'text':
                widget.config(
                    bg=colors['bg'],
                    fg=colors['fg'],
                    selectbackground=colors['select_bg'],
                    selectforeground=colors['select_fg'],
                    insertbackground=colors['fg']
                )
            elif widget_type == 'line_numbers':
                widget.config(
                    bg=colors['line_bg'],
                    fg=colors['line_fg']
                )
            elif widget_type == 'status':
                widget.config(
                    bg=colors['status_bg'],
                    fg=colors['status_fg']
                )
            elif widget_type == 'sidebar':
                widget.config(
                    bg=colors['sidebar_bg'],
                    fg=colors['sidebar_fg']
                )
            elif widget_type == 'toolbar':
                widget.config(
                    bg=colors['toolbar_bg']
                )
            elif widget_type == 'frame':
                widget.config(
                    bg=colors['bg']
                )
        except Exception as e:
            print(f"Error applying theme to widget: {e}")
    
    def create_styled_button(self, parent, text, command=None, **kwargs):
        """Create a styled button with current theme"""
        colors = self.get_colors()
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=colors['button_bg'],
            fg=colors['fg'],
            activebackground=colors['button_hover'],
            activeforeground=colors['fg'],
            relief='flat',
            bd=1,
            padx=8,
            pady=2,
            **kwargs
        )
        
        # Add hover effects
        def on_enter(e):
            button.config(bg=colors['button_hover'])
        
        def on_leave(e):
            button.config(bg=colors['button_bg'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button

# Global theme manager instance
theme_manager = ThemeManager()