# Advanced syntax highlighter for multiple languages
import re
import keyword
from config import Config
from ui.themes import theme_manager

class SyntaxHighlighter:
    """Advanced syntax highlighter supporting multiple programming languages"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.language = 'text'
        self.patterns = {}
        self.load_patterns()
        
        # Configure text tags for syntax highlighting
        self.configure_tags()
        
        # Register for theme changes
        theme_manager.add_observer(self.on_theme_change)
    
    def configure_tags(self):
        """Configure text tags for syntax highlighting"""
        colors = theme_manager.get_syntax_colors()
        font_family = self.text_widget.cget('font').split()[0] if self.text_widget.cget('font') else 'Consolas'
        font_size = int(self.text_widget.cget('font').split()[1]) if len(self.text_widget.cget('font').split()) > 1 else 12
        
        # Configure tags with colors
        for tag, color in colors.items():
            self.text_widget.tag_configure(
                tag,
                foreground=color,
                font=(font_family, font_size, 'bold' if tag in ['keyword', 'class', 'function'] else 'normal')
            )
    
    def load_patterns(self):
        """Load syntax patterns for different languages"""
        
        # Python patterns
        self.patterns['python'] = [
            ('keyword', r'\b(?:' + '|'.join(keyword.kwlist) + r')\b'),
            ('builtin', r'\b(?:abs|all|any|ascii|bin|bool|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip|__import__)\b'),
            ('string', r'(["\'])(?:(?=(\\?))\2.)*?\1'),
            ('string', r'(""".*?"""|\'\'\'.*?\'\'\')'),
            ('comment', r'#.*?$'),
            ('number', r'\b\d+\.?\d*\b'),
            ('function', r'\bdef\s+(\w+)'),
            ('class', r'\bclass\s+(\w+)'),
            ('operator', r'[+\-*/%=<>!&|^~]'),
            ('bracket', r'[(){}[\]]')
        ]
        
        # JavaScript patterns
        self.patterns['javascript'] = [
            ('keyword', r'\b(?:abstract|await|boolean|break|byte|case|catch|char|class|const|continue|debugger|default|delete|do|double|else|enum|export|extends|false|final|finally|float|for|function|goto|if|implements|import|in|instanceof|int|interface|let|long|native|new|null|package|private|protected|public|return|short|static|super|switch|synchronized|this|throw|throws|transient|true|try|typeof|var|void|volatile|while|with|yield)\b'),
            ('builtin', r'\b(?:Array|Boolean|Date|Error|Function|JSON|Math|Number|Object|RegExp|String|console|document|window|undefined|NaN|Infinity)\b'),
            ('string', r'(["\'])(?:(?=(\\?))\2.)*?\1'),
            ('string', r'`[^`]*`'),
            ('comment', r'//.*?$'),
            ('comment', r'/\*.*?\*/'),
            ('number', r'\b\d+\.?\d*\b'),
            ('function', r'\bfunction\s+(\w+)'),
            ('class', r'\bclass\s+(\w+)'),
            ('operator', r'[+\-*/%=<>!&|^~]'),
            ('bracket', r'[(){}[\]]')
        ]
        
        # HTML patterns
        self.patterns['html'] = [
            ('tag', r'</?[a-zA-Z][^>]*>'),
            ('attribute', r'\b[a-zA-Z-]+(?==)'),
            ('string', r'(["\'])(?:(?=(\\?))\2.)*?\1'),
            ('comment', r'<!--.*?-->'),
            ('bracket', r'[<>]')
        ]
        
        # CSS patterns
        self.patterns['css'] = [
            ('css_property', r'\b[a-zA-Z-]+(?=\s*:)'),
            ('css_value', r':\s*[^;}\n]+'),
            ('string', r'(["\'])(?:(?=(\\?))\2.)*?\1'),
            ('comment', r'/\*.*?\*/'),
            ('number', r'\b\d+(?:px|em|rem|%|vh|vw|pt|pc|in|cm|mm|ex|ch|vmin|vmax)?\b'),
            ('bracket', r'[{}()[\]]'),
            ('operator', r'[,:;]')
        ]
        
        # JSON patterns
        self.patterns['json'] = [
            ('string', r'(["\'])(?:(?=(\\?))\2.)*?\1'),
            ('number', r'\b\d+\.?\d*\b'),
            ('keyword', r'\b(?:true|false|null)\b'),
            ('bracket', r'[{}()[\]]'),
            ('operator', r'[,:;]')
        ]
        
        # C/C++ patterns
        self.patterns['c'] = [
            ('keyword', r'\b(?:auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b'),
            ('builtin', r'\b(?:printf|scanf|malloc|free|sizeof|strlen|strcpy|strcmp|strcat|fopen|fclose|fread|fwrite)\b'),
            ('string', r'(["\'])(?:(?=(\\?))\2.)*?\1'),
            ('comment', r'//.*?$'),
            ('comment', r'/\*.*?\*/'),
            ('number', r'\b\d+\.?\d*[fFlLuU]?\b'),
            ('operator', r'[+\-*/%=<>!&|^~]'),
            ('bracket', r'[(){}[\]]')
        ]
        
        # Add more language patterns as needed...
    
    def set_language(self, language):
        """Set the current language for syntax highlighting"""
        self.language = language.lower()
        self.highlight_all()
    
    def detect_language_from_extension(self, file_extension):
        """Detect language from file extension"""
        return Config.LANGUAGE_EXTENSIONS.get(file_extension.lower(), 'text')
    
    def highlight_all(self):
        """Highlight the entire text"""
        if self.language not in self.patterns:
            return
        
        # Clear existing tags
        for tag in theme_manager.get_syntax_colors().keys():
            self.text_widget.tag_remove(tag, '1.0', 'end')
        
        content = self.text_widget.get('1.0', 'end-1c')
        
        # Apply syntax highlighting patterns
        for tag, pattern in self.patterns[self.language]:
            for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.text_widget.tag_add(tag, start_idx, end_idx)
    
    def highlight_line(self, line_number):
        """Highlight a specific line (for performance)"""
        if self.language not in self.patterns:
            return
        
        # Get line content
        line_start = f"{line_number}.0"
        line_end = f"{line_number}.end"
        line_content = self.text_widget.get(line_start, line_end)
        
        # Clear existing tags on this line
        for tag in theme_manager.get_syntax_colors().keys():
            self.text_widget.tag_remove(tag, line_start, line_end)
        
        # Apply patterns to this line
        for tag, pattern in self.patterns[self.language]:
            for match in re.finditer(pattern, line_content):
                start_idx = f"{line_number}.{match.start()}"
                end_idx = f"{line_number}.{match.end()}"
                self.text_widget.tag_add(tag, start_idx, end_idx)
    
    def on_text_change(self, event=None):
        """Handle text changes for incremental highlighting"""
        # Get current line number
        current_line = self.text_widget.index('insert').split('.')[0]
        
        # Highlight current line and surrounding lines for context
        try:
            line_num = int(current_line)
            for i in range(max(1, line_num - 1), min(int(self.text_widget.index('end').split('.')[0]), line_num + 2)):
                self.highlight_line(i)
        except ValueError:
            pass
    
    def on_theme_change(self, theme_name):
        """Handle theme change"""
        self.configure_tags()
        self.highlight_all()

class CodeFolding:
    """Code folding functionality"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.folded_regions = {}
        self.fold_markers = {}
    
    def add_fold_markers(self):
        """Add fold markers to the text"""
        # This is a simplified implementation
        # In a full implementation, you'd parse the code structure
        pass
    
    def toggle_fold(self, line_number):
        """Toggle fold at a specific line"""
        if line_number in self.folded_regions:
            self.unfold_region(line_number)
        else:
            self.fold_region(line_number)
    
    def fold_region(self, start_line):
        """Fold a region starting at the given line"""
        # Simplified folding - in practice, you'd need to determine
        # the end of the foldable region based on indentation or braces
        end_line = start_line + 10  # Placeholder
        
        # Hide lines
        for i in range(start_line + 1, end_line + 1):
            self.text_widget.tag_add('folded', f"{i}.0", f"{i}.end+1c")
        
        self.text_widget.tag_config('folded', elide=True)
        self.folded_regions[start_line] = end_line
    
    def unfold_region(self, start_line):
        """Unfold a region"""
        if start_line in self.folded_regions:
            end_line = self.folded_regions[start_line]
            self.text_widget.tag_remove('folded', f"{start_line + 1}.0", f"{end_line}.end+1c")
            del self.folded_regions[start_line]