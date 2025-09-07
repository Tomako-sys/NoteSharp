# Auto-completion system for NoteSharp
import tkinter as tk
import re
import keyword
from pathlib import Path

class AutoComplete:
    """Basic auto-completion system"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.language = 'text'
        self.completion_window = None
        self.completion_list = []
        self.current_completions = []
        
        # Language-specific completions
        self.completions = {
            'python': {
                'keywords': keyword.kwlist,
                'builtins': ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 
                           'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 
                           'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 
                           'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 
                           'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 
                           'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 
                           'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 
                           'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 
                           'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 
                           'super', 'tuple', 'type', 'vars', 'zip'],
                'snippets': {
                    'def': 'def function_name():\n    pass',
                    'class': 'class ClassName:\n    def __init__(self):\n        pass',
                    'if': 'if condition:\n    pass',
                    'for': 'for item in iterable:\n    pass',
                    'while': 'while condition:\n    pass',
                    'try': 'try:\n    pass\nexcept Exception as e:\n    pass',
                    'with': 'with open("file.txt") as f:\n    pass'
                }
            },
            'javascript': {
                'keywords': ['abstract', 'await', 'boolean', 'break', 'byte', 'case', 'catch', 
                           'char', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 
                           'do', 'double', 'else', 'enum', 'export', 'extends', 'false', 'final', 
                           'finally', 'float', 'for', 'function', 'goto', 'if', 'implements', 
                           'import', 'in', 'instanceof', 'int', 'interface', 'let', 'long', 
                           'native', 'new', 'null', 'package', 'private', 'protected', 'public', 
                           'return', 'short', 'static', 'super', 'switch', 'synchronized', 'this', 
                           'throw', 'throws', 'transient', 'true', 'try', 'typeof', 'var', 'void', 
                           'volatile', 'while', 'with', 'yield'],
                'builtins': ['Array', 'Boolean', 'Date', 'Error', 'Function', 'JSON', 'Math', 
                           'Number', 'Object', 'RegExp', 'String', 'console', 'document', 
                           'window', 'undefined', 'NaN', 'Infinity'],
                'snippets': {
                    'function': 'function functionName() {\n    \n}',
                    'if': 'if (condition) {\n    \n}',
                    'for': 'for (let i = 0; i < length; i++) {\n    \n}',
                    'while': 'while (condition) {\n    \n}',
                    'try': 'try {\n    \n} catch (error) {\n    \n}',
                    'class': 'class ClassName {\n    constructor() {\n        \n    }\n}'
                }
            },
            'html': {
                'keywords': ['html', 'head', 'body', 'div', 'span', 'p', 'a', 'img', 'ul', 'ol', 
                           'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'tr', 'td', 'th', 
                           'form', 'input', 'button', 'select', 'option', 'textarea', 'script', 
                           'style', 'link', 'meta', 'title'],
                'snippets': {
                    'html5': '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Document</title>\n</head>\n<body>\n    \n</body>\n</html>',
                    'div': '<div>\n    \n</div>',
                    'form': '<form>\n    <input type="text" name="" id="">\n    <button type="submit">Submit</button>\n</form>'
                }
            },
            'css': {
                'keywords': ['color', 'background', 'font-size', 'font-family', 'margin', 'padding', 
                           'border', 'width', 'height', 'display', 'position', 'top', 'right', 
                           'bottom', 'left', 'float', 'clear', 'text-align', 'font-weight', 
                           'text-decoration', 'line-height', 'letter-spacing', 'word-spacing', 
                           'vertical-align', 'white-space', 'list-style', 'cursor', 'overflow', 
                           'visibility', 'z-index', 'opacity', 'transform', 'transition', 
                           'animation', 'box-shadow', 'border-radius', 'flex', 'grid'],
                'snippets': {
                    'flex': 'display: flex;\njustify-content: center;\nalign-items: center;',
                    'grid': 'display: grid;\ngrid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\ngap: 1rem;',
                    'center': 'margin: 0 auto;\ntext-align: center;'
                }
            }
        }
        
        # Bind events
        self.text_widget.bind('<KeyRelease>', self.on_key_release)
        self.text_widget.bind('<Button-1>', self.hide_completion)
    
    def set_language(self, language):
        """Set the current language for completions"""
        self.language = language.lower()
    
    def on_key_release(self, event):
        """Handle key release events"""
        if event.keysym in ['Up', 'Down', 'Left', 'Right', 'Return', 'Tab']:
            self.hide_completion()
            return
        
        # Get current word
        current_word = self.get_current_word()
        
        if len(current_word) >= 2:  # Start completion after 2 characters
            self.show_completion(current_word)
        else:
            self.hide_completion()
    
    def get_current_word(self):
        """Get the current word being typed"""
        cursor_pos = self.text_widget.index(tk.INSERT)
        line_start = cursor_pos.split('.')[0] + '.0'
        line_text = self.text_widget.get(line_start, cursor_pos)
        
        # Find the last word
        match = re.search(r'\b(\w+)$', line_text)
        return match.group(1) if match else ''
    
    def get_completions(self, prefix):
        """Get completions for the given prefix"""
        completions = []
        
        if self.language in self.completions:
            lang_completions = self.completions[self.language]
            
            # Add keywords
            if 'keywords' in lang_completions:
                completions.extend([kw for kw in lang_completions['keywords'] 
                                  if kw.startswith(prefix.lower())])
            
            # Add builtins
            if 'builtins' in lang_completions:
                completions.extend([bi for bi in lang_completions['builtins'] 
                                  if bi.lower().startswith(prefix.lower())])
            
            # Add snippets
            if 'snippets' in lang_completions:
                completions.extend([sn for sn in lang_completions['snippets'].keys() 
                                  if sn.startswith(prefix.lower())])
        
        # Add words from current document
        document_words = self.get_document_words()
        completions.extend([word for word in document_words 
                          if word.lower().startswith(prefix.lower()) and word != prefix])
        
        # Remove duplicates and sort
        completions = sorted(list(set(completions)))
        
        return completions[:10]  # Limit to 10 completions
    
    def get_document_words(self):
        """Extract words from the current document"""
        content = self.text_widget.get('1.0', 'end-1c')
        words = re.findall(r'\b\w{3,}\b', content)  # Words with 3+ characters
        return list(set(words))
    
    def show_completion(self, prefix):
        """Show completion popup"""
        completions = self.get_completions(prefix)
        
        if not completions:
            self.hide_completion()
            return
        
        # Hide existing completion window
        self.hide_completion()
        
        # Create completion window
        self.completion_window = tk.Toplevel(self.text_widget)
        self.completion_window.wm_overrideredirect(True)
        self.completion_window.configure(bg='white', relief='solid', bd=1)
        
        # Position the window
        cursor_pos = self.text_widget.index(tk.INSERT)
        x, y, _, _ = self.text_widget.bbox(cursor_pos)
        x += self.text_widget.winfo_rootx()
        y += self.text_widget.winfo_rooty() + 20
        
        self.completion_window.geometry(f"+{x}+{y}")
        
        # Create listbox with completions
        listbox = tk.Listbox(
            self.completion_window,
            height=min(len(completions), 8),
            width=max(len(max(completions, key=len)), 15),
            font=('Consolas', 10)
        )
        listbox.pack()
        
        for completion in completions:
            listbox.insert(tk.END, completion)
        
        # Select first item
        if completions:
            listbox.selection_set(0)
            listbox.activate(0)
        
        # Bind events
        listbox.bind('<Double-Button-1>', lambda e: self.insert_completion(prefix, listbox.get(listbox.curselection())))
        listbox.bind('<Return>', lambda e: self.insert_completion(prefix, listbox.get(listbox.curselection())))
        listbox.focus_set()
        
        self.current_completions = completions
    
    def hide_completion(self, event=None):
        """Hide completion popup"""
        if self.completion_window:
            self.completion_window.destroy()
            self.completion_window = None
            self.current_completions = []
    
    def insert_completion(self, prefix, completion):
        """Insert selected completion"""
        if not completion:
            return
        
        # Get cursor position
        cursor_pos = self.text_widget.index(tk.INSERT)
        
        # Calculate start position (beginning of current word)
        line_num, col_num = map(int, cursor_pos.split('.'))
        start_pos = f"{line_num}.{col_num - len(prefix)}"
        
        # Delete current prefix and insert completion
        self.text_widget.delete(start_pos, cursor_pos)
        
        # Check if it's a snippet
        if (self.language in self.completions and 
            'snippets' in self.completions[self.language] and 
            completion in self.completions[self.language]['snippets']):
            
            snippet = self.completions[self.language]['snippets'][completion]
            self.text_widget.insert(start_pos, snippet)
        else:
            self.text_widget.insert(start_pos, completion)
        
        self.hide_completion()
        self.text_widget.focus_set()