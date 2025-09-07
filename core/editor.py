# Enhanced text editor with modern features
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font
from datetime import datetime
import os
import re
from pathlib import Path

from config import Config
from ui.themes import theme_manager
from syntax.highlighter import SyntaxHighlighter, CodeFolding
from syntax.autocomplete import AutoComplete

class EnhancedTextEditor:
    """Enhanced text editor with modern features"""
    
    def __init__(self, root, on_tab_title_change=None, on_file_change=None):
        self.root = root
        self.file_path = None
        self.text_changed = False
        self.font_family = Config.DEFAULT_FONT_FAMILY
        self.font_size = Config.DEFAULT_FONT_SIZE
        self.on_tab_title_change = on_tab_title_change
        self.on_file_change = on_file_change
        self.locked = False
        self.read_only = False
        self.wrap_mode = 'word'
        self.show_line_numbers = True
        self.auto_save_enabled = False
        self._auto_save_job = None
        self.zoom_level = 0
        
        # Create the editor interface
        self.create_editor()
        
        # Initialize advanced features
        self.syntax_highlighter = SyntaxHighlighter(self.text)
        self.code_folding = CodeFolding(self.text)
        self.auto_complete = AutoComplete(self.text)
        
        # Register for theme changes
        theme_manager.add_observer(self.on_theme_change)
        
        # Update display
        self.update_line_numbers()
        self.update_status()
        self.apply_theme()
    
    def create_editor(self):
        """Create the editor interface"""
        # Main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # Editor area with line numbers
        editor_frame = tk.Frame(self.main_frame)
        editor_frame.pack(fill='both', expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            state='disabled',
            font=(self.font_family, self.font_size),
            wrap='none'
        )
        
        # Main text area
        self.text = tk.Text(
            editor_frame,
            wrap=self.wrap_mode,
            font=(self.font_family, self.font_size),
            undo=True,
            maxundo=50,
            tabs=('4c',)  # Set tab width to 4 characters
        )
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(editor_frame, orient='vertical')
        h_scrollbar = tk.Scrollbar(editor_frame, orient='horizontal')
        
        # Configure scrolling
        self.text.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.line_numbers.config(yscrollcommand=v_scrollbar.set)
        v_scrollbar.config(command=self.sync_scroll)
        h_scrollbar.config(command=self.text.xview)
        
        # Pack widgets
        if self.show_line_numbers:
            self.line_numbers.pack(side='left', fill='y')
        self.text.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Status bar
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(side='bottom', fill='x')
        
        self.status_left = tk.Label(self.status_frame, text="", anchor='w')
        self.status_left.pack(side='left', fill='x', expand=True)
        
        self.status_right = tk.Label(self.status_frame, text="", anchor='e')
        self.status_right.pack(side='right')
        
        # Bind events
        self.bind_events()
    
    def bind_events(self):
        """Bind keyboard and mouse events"""
        # Text change events
        self.text.bind('<KeyRelease>', self.on_text_change)
        self.text.bind('<<Modified>>', self.on_modified)
        self.text.bind('<ButtonRelease-1>', self.on_cursor_change)
        self.text.bind('<Configure>', lambda e: self.update_line_numbers())
        
        # Selection and cursor events
        self.text.bind('<<Selection>>', self.update_status)
        self.text.bind('<KeyRelease>', self.update_status)
        self.text.bind('<ButtonRelease-1>', self.update_status)
        
        # Scrolling synchronization
        self.text.bind('<MouseWheel>', self.sync_scrollbar)
        
        # Keyboard shortcuts
        self.text.bind('<Control-d>', lambda e: self.duplicate_line())
        self.text.bind('<Control-slash>', lambda e: self.toggle_comment())
        self.text.bind('<Control-equal>', lambda e: self.zoom_in())
        self.text.bind('<Control-plus>', lambda e: self.zoom_in())
        self.text.bind('<Control-minus>', lambda e: self.zoom_out())
        self.text.bind('<Control-0>', lambda e: self.reset_zoom())
        
        # Custom shortcuts
        self.text.bind('<Alt-Up>', lambda e: self.move_line_up())
        self.text.bind('<Alt-Down>', lambda e: self.move_line_down())
        self.text.bind('<Control-j>', lambda e: self.join_lines())
        self.text.bind('<Control-l>', lambda e: self.select_line())
    
    def sync_scroll(self, *args):
        """Synchronize scrolling between text and line numbers"""
        self.text.yview(*args)
        if self.show_line_numbers:
            self.line_numbers.yview(*args)
    
    def sync_scrollbar(self, event):
        """Synchronize scrollbar with line numbers"""
        if self.show_line_numbers:
            self.line_numbers.yview_moveto(self.text.yview()[0])
        return 'break'
    
    def update_line_numbers(self):
        """Update line numbers display"""
        if not self.show_line_numbers:
            return
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        
        # Get number of lines
        line_count = int(self.text.index('end-1c').split('.')[0])
        
        # Generate line numbers
        line_numbers = '\n'.join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert(1.0, line_numbers)
        
        self.line_numbers.config(state='disabled')
    
    def update_status(self, event=None):
        """Update status bar information"""
        try:
            # Get text content
            content = self.text.get(1.0, tk.END)
            
            # Calculate statistics
            char_count = len(content.rstrip('\n'))
            line_count = int(self.text.index('end-1c').split('.')[0])
            word_count = len(content.split())
            paragraph_count = content.count('\n\n') + 1
            
            # Get selection info
            try:
                selection = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
                selection_count = len(selection)
            except tk.TclError:
                selection_count = 0
            
            # Get cursor position
            cursor_pos = self.text.index(tk.INSERT)
            line_num, col_num = cursor_pos.split('.')
            
            # Update status bar
            left_status = f"Lines: {line_count} | Words: {word_count} | Characters: {char_count}"
            if selection_count > 0:
                left_status += f" | Selected: {selection_count}"
            
            right_status = f"Ln {line_num}, Col {int(col_num) + 1}"
            if self.file_path:
                encoding = "UTF-8"  # Default encoding
                right_status += f" | {encoding}"
            
            # Add language info
            if hasattr(self, 'syntax_highlighter'):
                language = self.syntax_highlighter.language.title()
                right_status += f" | {language}"
            
            self.status_left.config(text=left_status)
            self.status_right.config(text=right_status)
            
        except Exception as e:
            print(f"Error updating status: {e}")
    
    def on_text_change(self, event=None):
        """Handle text change events"""
        self.text_changed = True
        self.update_line_numbers()
        self.update_status()
        
        # Update syntax highlighting
        if hasattr(self, 'syntax_highlighter'):
            self.syntax_highlighter.on_text_change(event)
        
        # Update auto-complete
        if hasattr(self, 'auto_complete'):
            # Only show auto-complete for certain key events
            if event and hasattr(event, 'keysym') and len(event.keysym) == 1:
                pass  # Auto-complete handles its own key events
    
    def on_modified(self, event=None):
        """Handle text modified event"""
        if self.text.edit_modified():
            self.text_changed = True
            if self.on_file_change:
                self.on_file_change(self.file_path, True)
            self.text.edit_modified(False)
    
    def on_cursor_change(self, event=None):
        """Handle cursor position changes"""
        self.update_status()
        self.update_line_numbers()
    
    def open_file(self, file_path=None):
        """Open a file"""
        if not file_path:
            file_path = filedialog.askopenfilename(
                filetypes=[
                    ("All Files", "*.*"),
                    ("Python Files", "*.py"),
                    ("JavaScript Files", "*.js"),
                    ("HTML Files", "*.html"),
                    ("CSS Files", "*.css"),
                    ("Text Files", "*.txt"),
                    ("Markdown Files", "*.md"),
                    ("JSON Files", "*.json"),
                    ("XML Files", "*.xml")
                ]
            )
        
        if not file_path:
            return False
        
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > Config.MAX_FILE_SIZE:
                if not messagebox.askyesno(
                    "Large File",
                    f"File is {file_size // (1024*1024)}MB. This may affect performance. Continue?"
                ):
                    return False
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Clear current content and insert new
            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, content)
            
            # Update file info
            self.file_path = file_path
            self.text_changed = False
            
            # Update tab title
            if self.on_tab_title_change:
                filename = os.path.basename(file_path)
                if self.locked:
                    filename += " 🔒"
                self.on_tab_title_change(filename)
            
            # Detect and set language for syntax highlighting
            if hasattr(self, 'syntax_highlighter'):
                ext = Path(file_path).suffix
                language = self.syntax_highlighter.detect_language_from_extension(ext)
                self.syntax_highlighter.set_language(language)
                
                if hasattr(self, 'auto_complete'):
                    self.auto_complete.set_language(language)
            
            # Update displays
            self.update_line_numbers()
            self.update_status()
            
            # Notify file change
            if self.on_file_change:
                self.on_file_change(file_path, False)
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file: {str(e)}")
            return False
    
    def save_file(self, file_path=None):
        """Save the current file"""
        if not file_path and not self.file_path:
            return self.save_file_as()
        
        target_path = file_path or self.file_path
        
        try:
            content = self.text.get(1.0, tk.END)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.file_path = target_path
            self.text_changed = False
            
            # Update tab title
            if self.on_tab_title_change:
                filename = os.path.basename(target_path)
                if self.locked:
                    filename += " 🔒"
                self.on_tab_title_change(filename)
            
            # Notify file change
            if self.on_file_change:
                self.on_file_change(target_path, False)
            
            messagebox.showinfo("Success", "File saved successfully!")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot save file: {str(e)}")
            return False
    
    def save_file_as(self):
        """Save file with a new name"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("JavaScript Files", "*.js"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("Markdown Files", "*.md"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            return self.save_file(file_path)
        return False
    
    def ask_save_changes(self):
        """Ask user to save changes before closing"""
        if not self.text_changed:
            return True
        
        result = messagebox.askyesnocancel(
            "Unsaved Changes",
            "Do you want to save your changes before continuing?"
        )
        
        if result is None:  # Cancel
            return False
        elif result is True:  # Yes
            return self.save_file()
        else:  # No
            return True
    
    def toggle_word_wrap(self):
        """Toggle word wrapping"""
        self.wrap_mode = 'none' if self.wrap_mode == 'word' else 'word'
        self.text.config(wrap=self.wrap_mode)
    
    def toggle_line_numbers(self):
        """Toggle line numbers visibility"""
        self.show_line_numbers = not self.show_line_numbers
        
        if self.show_line_numbers:
            self.line_numbers.pack(side='left', fill='y', before=self.text)
            self.update_line_numbers()
        else:
            self.line_numbers.pack_forget()
    
    def set_read_only(self, read_only=True):
        """Set read-only mode"""
        self.read_only = read_only
        self.text.config(state=tk.DISABLED if read_only else tk.NORMAL)
    
    def lock_tab(self, locked=True):
        """Lock/unlock the tab"""
        self.locked = locked
        
        # Update tab title
        if self.on_tab_title_change and self.file_path:
            filename = os.path.basename(self.file_path)
            if locked:
                filename += " 🔒"
            self.on_tab_title_change(filename)
    
    def duplicate_line(self):
        """Duplicate the current line"""
        cursor_pos = self.text.index(tk.INSERT)
        line_num = int(cursor_pos.split('.')[0])
        line_start = f"{line_num}.0"
        line_end = f"{line_num}.end"
        line_content = self.text.get(line_start, line_end)
        
        self.text.insert(line_end, f"\n{line_content}")
        return 'break'
    
    def toggle_comment(self):
        """Toggle comment on current line or selection"""
        try:
            # Get current language for comment style
            comment_chars = {
                'python': '#',
                'javascript': '//',
                'java': '//',
                'c': '//',
                'cpp': '//',
                'css': '/*',
                'html': '<!--',
                'text': '#'
            }
            
            language = getattr(self.syntax_highlighter, 'language', 'text')
            comment_char = comment_chars.get(language, '#')
            
            # Get selection or current line
            try:
                start = self.text.index(tk.SEL_FIRST)
                end = self.text.index(tk.SEL_LAST)
            except tk.TclError:
                # No selection, use current line
                cursor_pos = self.text.index(tk.INSERT)
                line_num = cursor_pos.split('.')[0]
                start = f"{line_num}.0"
                end = f"{line_num}.end"
            
            # Get selected lines
            start_line = int(start.split('.')[0])
            end_line = int(end.split('.')[0])
            
            # Check if lines are commented
            lines_commented = True
            for line_num in range(start_line, end_line + 1):
                line_content = self.text.get(f"{line_num}.0", f"{line_num}.end").strip()
                if line_content and not line_content.startswith(comment_char):
                    lines_commented = False
                    break
            
            # Toggle comments
            for line_num in range(start_line, end_line + 1):
                line_start = f"{line_num}.0"
                line_content = self.text.get(line_start, f"{line_num}.end")
                
                if lines_commented:
                    # Remove comment
                    if line_content.strip().startswith(comment_char):
                        # Find the comment character and remove it
                        comment_pos = line_content.find(comment_char)
                        new_content = line_content[:comment_pos] + line_content[comment_pos + len(comment_char):].lstrip()
                        self.text.delete(line_start, f"{line_num}.end")
                        self.text.insert(line_start, new_content)
                else:
                    # Add comment
                    if line_content.strip():  # Only comment non-empty lines
                        # Find first non-whitespace character
                        stripped = line_content.lstrip()
                        if stripped:
                            indent = line_content[:len(line_content) - len(stripped)]
                            new_content = indent + comment_char + ' ' + stripped
                            self.text.delete(line_start, f"{line_num}.end")
                            self.text.insert(line_start, new_content)
        
        except Exception as e:
            print(f"Error toggling comment: {e}")
        
        return 'break'
    
    def zoom_in(self):
        """Increase font size"""
        self.zoom_level += 1
        new_size = self.font_size + self.zoom_level
        self.text.config(font=(self.font_family, new_size))
        if self.show_line_numbers:
            self.line_numbers.config(font=(self.font_family, new_size))
        return 'break'
    
    def zoom_out(self):
        """Decrease font size"""
        self.zoom_level -= 1
        new_size = max(8, self.font_size + self.zoom_level)
        self.text.config(font=(self.font_family, new_size))
        if self.show_line_numbers:
            self.line_numbers.config(font=(self.font_family, new_size))
        return 'break'
    
    def reset_zoom(self):
        """Reset font size to default"""
        self.zoom_level = 0
        self.text.config(font=(self.font_family, self.font_size))
        if self.show_line_numbers:
            self.line_numbers.config(font=(self.font_family, self.font_size))
        return 'break'
    
    def move_line_up(self):
        """Move current line up"""
        cursor_pos = self.text.index(tk.INSERT)
        line_num = int(cursor_pos.split('.')[0])
        
        if line_num > 1:
            # Get current line content
            current_line = self.text.get(f"{line_num}.0", f"{line_num}.end+1c")
            # Get previous line content
            prev_line = self.text.get(f"{line_num-1}.0", f"{line_num-1}.end+1c")
            
            # Replace both lines
            self.text.delete(f"{line_num-1}.0", f"{line_num}.end+1c")
            self.text.insert(f"{line_num-1}.0", current_line + prev_line.rstrip('\n'))
            
            # Move cursor
            col_num = cursor_pos.split('.')[1]
            self.text.mark_set(tk.INSERT, f"{line_num-1}.{col_num}")
        
        return 'break'
    
    def move_line_down(self):
        """Move current line down"""
        cursor_pos = self.text.index(tk.INSERT)
        line_num = int(cursor_pos.split('.')[0])
        max_line = int(self.text.index('end-1c').split('.')[0])
        
        if line_num < max_line:
            # Get current line content
            current_line = self.text.get(f"{line_num}.0", f"{line_num}.end+1c")
            # Get next line content
            next_line = self.text.get(f"{line_num+1}.0", f"{line_num+1}.end+1c")
            
            # Replace both lines
            self.text.delete(f"{line_num}.0", f"{line_num+1}.end+1c")
            self.text.insert(f"{line_num}.0", next_line.rstrip('\n') + '\n' + current_line.rstrip('\n'))
            
            # Move cursor
            col_num = cursor_pos.split('.')[1]
            self.text.mark_set(tk.INSERT, f"{line_num+1}.{col_num}")
        
        return 'break'
    
    def join_lines(self):
        """Join current line with next line"""
        cursor_pos = self.text.index(tk.INSERT)
        line_num = int(cursor_pos.split('.')[0])
        max_line = int(self.text.index('end-1c').split('.')[0])
        
        if line_num < max_line:
            # Get current and next line
            current_line = self.text.get(f"{line_num}.0", f"{line_num}.end")
            next_line = self.text.get(f"{line_num+1}.0", f"{line_num+1}.end")
            
            # Join lines with space
            joined_line = current_line + ' ' + next_line.lstrip()
            
            # Replace both lines
            self.text.delete(f"{line_num}.0", f"{line_num+1}.end")
            self.text.insert(f"{line_num}.0", joined_line)
        
        return 'break'
    
    def select_line(self):
        """Select the current line"""
        cursor_pos = self.text.index(tk.INSERT)
        line_num = cursor_pos.split('.')[0]
        self.text.tag_add(tk.SEL, f"{line_num}.0", f"{line_num}.end")
        return 'break'
    
    def goto_line(self):
        """Go to a specific line number"""
        line_num = simpledialog.askinteger(
            "Go to Line",
            "Enter line number:",
            minvalue=1,
            maxvalue=int(self.text.index('end-1c').split('.')[0])
        )
        
        if line_num:
            self.text.mark_set(tk.INSERT, f"{line_num}.0")
            self.text.see(f"{line_num}.0")
            self.text.focus_set()
    
    def insert_timestamp(self):
        """Insert current timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text.insert(tk.INSERT, timestamp)
    
    def apply_theme(self):
        """Apply the current theme"""
        colors = theme_manager.get_colors()
        
        # Apply to text widget
        theme_manager.apply_theme_to_widget(self.text, 'text')
        
        # Apply to line numbers
        if self.show_line_numbers:
            theme_manager.apply_theme_to_widget(self.line_numbers, 'line_numbers')
        
        # Apply to status bar
        theme_manager.apply_theme_to_widget(self.status_left, 'status')
        theme_manager.apply_theme_to_widget(self.status_right, 'status')
        theme_manager.apply_theme_to_widget(self.status_frame, 'frame')
        
        # Apply to main frame
        theme_manager.apply_theme_to_widget(self.main_frame, 'frame')
    
    def on_theme_change(self, theme_name):
        """Handle theme change"""
        self.apply_theme()
        
        # Update syntax highlighting colors
        if hasattr(self, 'syntax_highlighter'):
            self.syntax_highlighter.on_theme_change(theme_name)
    
    def enable_auto_save(self, interval=None):
        """Enable auto-save functionality"""
        if interval is None:
            interval = Config.AUTO_SAVE_INTERVAL
        
        self.disable_auto_save()  # Stop any existing auto-save
        
        def auto_save():
            if self.file_path and self.text_changed:
                try:
                    content = self.text.get(1.0, tk.END)
                    with open(self.file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.text_changed = False
                except Exception as e:
                    print(f"Auto-save error: {e}")
            
            # Schedule next auto-save
            self._auto_save_job = self.text.after(interval * 1000, auto_save)
        
        self.auto_save_enabled = True
        auto_save()
    
    def disable_auto_save(self):
        """Disable auto-save functionality"""
        if self._auto_save_job:
            self.text.after_cancel(self._auto_save_job)
            self._auto_save_job = None
        self.auto_save_enabled = False
    
    def get_content(self):
        """Get the current text content"""
        return self.text.get(1.0, tk.END)
    
    def set_content(self, content):
        """Set the text content"""
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, content)
        self.text_changed = True
        self.update_line_numbers()
        self.update_status()
    
    def find_text(self, search_term, start_pos='1.0'):
        """Find text in the editor"""
        pos = self.text.search(search_term, start_pos, stopindex=tk.END)
        if pos:
            end_pos = f"{pos}+{len(search_term)}c"
            self.text.tag_remove('found', '1.0', tk.END)
            self.text.tag_add('found', pos, end_pos)
            self.text.tag_config('found', background='yellow', foreground='black')
            self.text.see(pos)
            self.text.mark_set(tk.INSERT, end_pos)
            return pos
        return None
    
    def replace_text(self, old_text, new_text, all_occurrences=False):
        """Replace text in the editor"""
        if all_occurrences:
            content = self.text.get(1.0, tk.END)
            new_content = content.replace(old_text, new_text)
            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, new_content)
            count = content.count(old_text)
            return count
        else:
            pos = self.find_text(old_text)
            if pos:
                end_pos = f"{pos}+{len(old_text)}c"
                self.text.delete(pos, end_pos)
                self.text.insert(pos, new_text)
                return 1
            return 0