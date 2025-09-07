# File explorer sidebar for NoteSharp
import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path
from ui.themes import theme_manager
from config import Config

class FileExplorer:
    """File explorer sidebar with tree view"""
    
    def __init__(self, parent, on_file_select=None):
        self.parent = parent
        self.on_file_select = on_file_select
        self.sidebar_frame = None
        self.tree = None
        self.current_path = Path.home()
        self.visible = True
        
        self.create_sidebar()
        theme_manager.add_observer(self.on_theme_change)
    
    def create_sidebar(self):
        """Create the sidebar with file tree"""
        if self.sidebar_frame:
            self.sidebar_frame.destroy()
        
        colors = theme_manager.get_colors()
        
        self.sidebar_frame = tk.Frame(
            self.parent,
            bg=colors['sidebar_bg'],
            width=Config.SIDEBAR_WIDTH
        )
        self.sidebar_frame.pack(side='left', fill='y')
        self.sidebar_frame.pack_propagate(False)
        
        # Header
        header_frame = tk.Frame(self.sidebar_frame, bg=colors['sidebar_bg'])
        header_frame.pack(fill='x', padx=5, pady=5)
        
        title_label = tk.Label(
            header_frame,
            text="📁 Explorer",
            bg=colors['sidebar_bg'],
            fg=colors['sidebar_fg'],
            font=('Segoe UI', 10, 'bold')
        )
        title_label.pack(side='left')
        
        # Path navigation
        path_frame = tk.Frame(self.sidebar_frame, bg=colors['sidebar_bg'])
        path_frame.pack(fill='x', padx=5, pady=2)
        
        self.path_var = tk.StringVar(value=str(self.current_path))
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.path_var,
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 9)
        )
        path_entry.pack(fill='x')
        path_entry.bind('<Return>', self.on_path_change)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.sidebar_frame, bg=colors['sidebar_bg'])
        nav_frame.pack(fill='x', padx=5, pady=2)
        
        up_button = theme_manager.create_styled_button(
            nav_frame,
            "↑ Up",
            command=self.go_up
        )
        up_button.pack(side='left', padx=2)
        
        home_button = theme_manager.create_styled_button(
            nav_frame,
            "🏠 Home",
            command=self.go_home
        )
        home_button.pack(side='left', padx=2)
        
        refresh_button = theme_manager.create_styled_button(
            nav_frame,
            "🔄",
            command=self.refresh
        )
        refresh_button.pack(side='right')
        
        # File tree
        tree_frame = tk.Frame(self.sidebar_frame, bg=colors['sidebar_bg'])
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure ttk style for tree
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Treeview",
            background=colors['bg'],
            foreground=colors['fg'],
            fieldbackground=colors['bg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg']
        )
        style.configure(
            "Treeview.Heading",
            background=colors['sidebar_bg'],
            foreground=colors['sidebar_fg']
        )
        
        self.tree = ttk.Treeview(tree_frame, show='tree')
        self.tree.pack(fill='both', expand=True)
        
        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-1>', self.on_single_click)
        
        self.populate_tree()
    
    def populate_tree(self):
        """Populate the tree with files and folders"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Add parent directory if not at root
            if self.current_path.parent != self.current_path:
                self.tree.insert('', 'end', text='..', values=['parent'], tags=['folder'])
            
            # Get directory contents
            items = []
            try:
                for item in self.current_path.iterdir():
                    items.append(item)
            except PermissionError:
                pass
            
            # Sort: folders first, then files
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in items:
                if item.name.startswith('.'):
                    continue  # Skip hidden files
                
                if item.is_dir():
                    icon = "📁"
                    tags = ['folder']
                else:
                    icon = self.get_file_icon(item.suffix)
                    tags = ['file']
                
                self.tree.insert(
                    '',
                    'end',
                    text=f"{icon} {item.name}",
                    values=[str(item)],
                    tags=tags
                )
        
        except Exception as e:
            print(f"Error populating tree: {e}")
    
    def get_file_icon(self, extension):
        """Get icon for file based on extension"""
        icons = {
            '.py': '🐍',
            '.js': '📜',
            '.html': '🌐',
            '.css': '🎨',
            '.json': '📋',
            '.txt': '📄',
            '.md': '📝',
            '.xml': '📊',
            '.yaml': '⚙️',
            '.yml': '⚙️',
            '.cpp': '⚡',
            '.c': '⚡',
            '.java': '☕',
            '.php': '🐘',
            '.rb': '💎',
            '.go': '🔷',
            '.rs': '🦀',
            '.sql': '🗄️'
        }
        return icons.get(extension.lower(), '📄')
    
    def on_double_click(self, event):
        """Handle double click on tree item"""
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        
        if values:
            path = Path(values[0])
            
            if values[0] == 'parent':
                self.go_up()
            elif path.is_dir():
                self.current_path = path
                self.path_var.set(str(self.current_path))
                self.populate_tree()
            else:
                # Open file
                if self.on_file_select:
                    self.on_file_select(str(path))
    
    def on_single_click(self, event):
        """Handle single click on tree item"""
        pass
    
    def on_path_change(self, event):
        """Handle path change in entry"""
        new_path = Path(self.path_var.get())
        if new_path.exists() and new_path.is_dir():
            self.current_path = new_path
            self.populate_tree()
    
    def go_up(self):
        """Go to parent directory"""
        if self.current_path.parent != self.current_path:
            self.current_path = self.current_path.parent
            self.path_var.set(str(self.current_path))
            self.populate_tree()
    
    def go_home(self):
        """Go to home directory"""
        self.current_path = Path.home()
        self.path_var.set(str(self.current_path))
        self.populate_tree()
    
    def refresh(self):
        """Refresh the current directory"""
        self.populate_tree()
    
    def toggle_visibility(self):
        """Toggle sidebar visibility"""
        if self.visible:
            self.sidebar_frame.pack_forget()
            self.visible = False
        else:
            self.sidebar_frame.pack(side='left', fill='y')
            self.visible = True
        return self.visible
    
    def on_theme_change(self, theme_name):
        """Handle theme change"""
        self.create_sidebar()
    
    def get_frame(self):
        """Get the sidebar frame"""
        return self.sidebar_frame