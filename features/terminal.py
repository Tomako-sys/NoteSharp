# Integrated terminal for NoteSharp
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import os
import platform
from ui.themes import theme_manager
from config import Config

class IntegratedTerminal:
    """Integrated terminal panel"""
    
    def __init__(self, parent):
        self.parent = parent
        self.terminal_frame = None
        self.output_text = None
        self.command_entry = None
        self.current_directory = os.getcwd()
        self.command_history = []
        self.history_index = -1
        self.visible = False
        self.process = None
        
        self.create_terminal()
        theme_manager.add_observer(self.on_theme_change)
    
    def create_terminal(self):
        """Create the terminal interface"""
        if self.terminal_frame:
            self.terminal_frame.destroy()
        
        colors = theme_manager.get_colors()
        
        self.terminal_frame = tk.Frame(self.parent, bg=colors['bg'], height=200)
        
        # Terminal header
        header_frame = tk.Frame(self.terminal_frame, bg=colors['toolbar_bg'], height=25)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="⚡ Terminal",
            bg=colors['toolbar_bg'],
            fg=colors['fg'],
            font=('Segoe UI', 9, 'bold')
        )
        title_label.pack(side='left', padx=5, pady=2)
        
        # Terminal controls
        clear_btn = theme_manager.create_styled_button(
            header_frame,
            "Clear",
            command=self.clear_terminal
        )
        clear_btn.pack(side='right', padx=2, pady=1)
        
        # Output area with scrollbar
        output_frame = tk.Frame(self.terminal_frame, bg=colors['bg'])
        output_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        self.output_text = tk.Text(
            output_frame,
            bg='#000000',
            fg='#FFFFFF',
            font=('Consolas', 10),
            state='disabled',
            wrap='word'
        )
        self.output_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(output_frame, command=self.output_text.yview)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Command input area
        input_frame = tk.Frame(self.terminal_frame, bg=colors['bg'])
        input_frame.pack(fill='x', padx=2, pady=2)
        
        # Current directory label
        self.dir_label = tk.Label(
            input_frame,
            text=f"{os.path.basename(self.current_directory)} $",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Consolas', 10, 'bold')
        )
        self.dir_label.pack(side='left')
        
        # Command entry
        self.command_entry = tk.Entry(
            input_frame,
            bg='#1E1E1E',
            fg='#FFFFFF',
            font=('Consolas', 10),
            insertbackground='#FFFFFF'
        )
        self.command_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Bind events
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.bind('<Up>', self.history_up)
        self.command_entry.bind('<Down>', self.history_down)
        self.command_entry.bind('<Tab>', self.auto_complete)
        
        # Initial welcome message
        self.append_output(f"NoteSharp Terminal - {platform.system()} {platform.release()}\n")
        self.append_output(f"Current directory: {self.current_directory}\n")
        self.append_output("Type 'help' for available commands.\n\n")
    
    def toggle_visibility(self):
        """Toggle terminal visibility"""
        if self.visible:
            self.terminal_frame.pack_forget()
            self.visible = False
        else:
            self.terminal_frame.pack(side='bottom', fill='x')
            self.visible = True
            self.command_entry.focus_set()
        return self.visible
    
    def execute_command(self, event=None):
        """Execute a terminal command"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Add to history
        if command not in self.command_history:
            self.command_history.append(command)
        self.history_index = -1
        
        # Clear command entry
        self.command_entry.delete(0, tk.END)
        
        # Display command
        self.append_output(f"{os.path.basename(self.current_directory)} $ {command}\n", 'command')
        
        # Handle built-in commands
        if command.lower() in ['help', '?']:
            self.show_help()
            return
        elif command.lower() == 'clear':
            self.clear_terminal()
            return
        elif command.startswith('cd '):
            self.change_directory(command[3:].strip())
            return
        elif command.lower() == 'pwd':
            self.append_output(f"{self.current_directory}\n")
            return
        elif command.lower() == 'ls' or command.lower() == 'dir':
            self.list_directory()
            return
        
        # Execute system command
        self.execute_system_command(command)
    
    def execute_system_command(self, command):
        """Execute a system command in a separate thread"""
        def run_command():
            try:
                # Use shell=True for Windows compatibility
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=self.current_directory,
                    bufsize=1,
                    universal_newlines=True
                )
                
                self.process = process
                
                # Read output in real-time
                for line in iter(process.stdout.readline, ''):
                    if line:
                        self.parent.after(0, lambda l=line: self.append_output(l))
                
                process.wait()
                self.process = None
                
                if process.returncode != 0:
                    self.parent.after(0, lambda: self.append_output(f"\nCommand exited with code {process.returncode}\n", 'error'))
                
            except Exception as e:
                self.parent.after(0, lambda: self.append_output(f"Error: {str(e)}\n", 'error'))
        
        # Run in separate thread
        thread = threading.Thread(target=run_command, daemon=True)
        thread.start()
    
    def change_directory(self, path):
        """Change current directory"""
        try:        
            if path == '..':
                new_path = os.path.dirname(self.current_directory)
            elif path == '~':
                new_path = os.path.expanduser('~')
            elif os.path.isabs(path):
                new_path = path
            else:
                new_path = os.path.join(self.current_directory, path)
            
            if os.path.isdir(new_path):
                self.current_directory = os.path.abspath(new_path)
                self.dir_label.config(text=f"{os.path.basename(self.current_directory)} $")
                self.append_output(f"Changed to: {self.current_directory}\n")
            else:
                self.append_output(f"Directory not found: {path}\n", 'error')
        
        except Exception as e:
            self.append_output(f"Error changing directory: {str(e)}\n", 'error')
    
    def list_directory(self):
        """List current directory contents"""
        try:
            items = os.listdir(self.current_directory)
            items.sort()
            
            for item in items:
                item_path = os.path.join(self.current_directory, item)
                if os.path.isdir(item_path):
                    self.append_output(f"📁 {item}\n", 'directory')
                else:
                    self.append_output(f"📄 {item}\n")
        
        except Exception as e:
            self.append_output(f"Error listing directory: {str(e)}\n", 'error')
    
    def show_help(self):
        """Show available commands"""
        help_text = """
Available commands:
  help, ?          - Show this help message
  clear            - Clear terminal output
  cd <path>        - Change directory
  pwd              - Show current directory
  ls, dir          - List directory contents
  
All other commands are passed to the system shell.
Use Up/Down arrows to navigate command history.
Use Tab for basic auto-completion.

"""
        self.append_output(help_text)
    
    def append_output(self, text, tag='normal'):
        """Append text to output area"""
        self.output_text.config(state='normal')
        
        # Configure tags for different text types
        if tag == 'command':
            self.output_text.tag_config('command', foreground='#00FF00')
        elif tag == 'error':
            self.output_text.tag_config('error', foreground='#FF6B6B')
        elif tag == 'directory':
            self.output_text.tag_config('directory', foreground='#4DABF7')
        
        self.output_text.insert(tk.END, text, tag)
        self.output_text.config(state='disabled')
        self.output_text.see(tk.END)
    
    def clear_terminal(self):
        """Clear terminal output"""
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.append_output(f"Terminal cleared - Current directory: {self.current_directory}\n\n")
    
    def history_up(self, event):
        """Navigate up in command history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            command = self.command_history[-(self.history_index + 1)]
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, command)
        return 'break'
    
    def history_down(self, event):
        """Navigate down in command history"""
        if self.history_index > 0:
            self.history_index -= 1
            command = self.command_history[-(self.history_index + 1)]
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, command)
        elif self.history_index == 0:
            self.history_index = -1
            self.command_entry.delete(0, tk.END)
        return 'break'
    
    def auto_complete(self, event):
        """Basic auto-completion for file/directory names"""
        current_text = self.command_entry.get()
        cursor_pos = self.command_entry.index(tk.INSERT)
        
        # Simple file completion
        try:
            words = current_text.split()
            if words:
                last_word = words[-1]
                if '/' in last_word or '\\' in last_word:
                    # Path completion
                    dir_path = os.path.dirname(last_word)
                    if not dir_path:
                        dir_path = self.current_directory
                    elif not os.path.isabs(dir_path):
                        dir_path = os.path.join(self.current_directory, dir_path)
                    
                    if os.path.isdir(dir_path):
                        prefix = os.path.basename(last_word)
                        items = [item for item in os.listdir(dir_path) 
                                if item.startswith(prefix)]
                        
                        if len(items) == 1:
                            # Complete the path
                            completion = items[0]
                            new_text = current_text.replace(last_word, 
                                os.path.join(os.path.dirname(last_word), completion))
                            self.command_entry.delete(0, tk.END)
                            self.command_entry.insert(0, new_text)
        
        except Exception:
            pass
        
        return 'break'
    
    def on_theme_change(self, theme_name):
        """Handle theme change"""
        if self.terminal_frame:
            self.create_terminal()
    
    def get_frame(self):
        """Get the terminal frame"""
        return self.terminal_frame