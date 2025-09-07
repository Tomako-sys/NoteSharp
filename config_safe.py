# NoteSharp Configuration - GUI Safe Version
import os

class Config:
    """Global configuration for NoteSharp"""
    
    # Application info
    APP_NAME = "NoteSharp Pro"
    VERSION = "2.0.0"
    
    # Default settings
    DEFAULT_FONT_FAMILY = "Consolas"
    DEFAULT_FONT_SIZE = 12
    DEFAULT_THEME = "light"
    DEFAULT_LANGUAGE = "en"
    
    # File settings
    MAX_RECENT_FILES = 15
    AUTO_SAVE_INTERVAL = 120  # seconds
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # UI settings
    SIDEBAR_WIDTH = 250
    MIN_WINDOW_WIDTH = 1000
    MIN_WINDOW_HEIGHT = 600
    
    # Color schemes
    THEMES = {
        'light': {
            'bg': '#FFFFFF',
            'fg': '#000000',
            'select_bg': '#316AC5',
            'select_fg': '#FFFFFF',
            'line_bg': '#F5F5F5',
            'line_fg': '#555555',
            'status_bg': '#E1E1E1',
            'status_fg': '#000000',
            'sidebar_bg': '#F0F0F0',
            'sidebar_fg': '#000000',
            'toolbar_bg': '#E8E8E8',
            'button_bg': '#D0D0D0',
            'button_hover': '#C0C0C0',
            'border': '#CCCCCC'
        },
        'dark': {
            'bg': '#2B2B2B',
            'fg': '#FFFFFF',
            'select_bg': '#4A90E2',
            'select_fg': '#FFFFFF',
            'line_bg': '#1E1E1E',
            'line_fg': '#CCCCCC',
            'status_bg': '#1A1A1A',
            'status_fg': '#FFFFFF',
            'sidebar_bg': '#252526',
            'sidebar_fg': '#CCCCCC',
            'toolbar_bg': '#2D2D30',
            'button_bg': '#3C3C3C',
            'button_hover': '#4C4C4C',
            'border': '#464647'
        },
        'monokai': {
            'bg': '#272822',
            'fg': '#F8F8F2',
            'select_bg': '#49483E',
            'select_fg': '#F8F8F2',
            'line_bg': '#1E1F1C',
            'line_fg': '#90908A',
            'status_bg': '#1A1A1A',
            'status_fg': '#F8F8F2',
            'sidebar_bg': '#1E1F1C',
            'sidebar_fg': '#F8F8F2',
            'toolbar_bg': '#383830',
            'button_bg': '#49483E',
            'button_hover': '#5A5A52',
            'border': '#49483E'
        }
    }
    
    # Syntax highlighting colors
    SYNTAX_COLORS = {
        'light': {
            'keyword': '#0000FF',
            'string': '#008000',
            'comment': '#808080',
            'number': '#FF0000',
            'function': '#8B008B',
            'class': '#2E8B57',
            'builtin': '#800080',
            'operator': '#000000',
            'bracket': '#000000',
            'tag': '#800000',
            'attribute': '#008080',
            'css_property': '#0000FF',
            'css_value': '#008000'
        },
        'dark': {
            'keyword': '#569CD6',
            'string': '#CE9178',
            'comment': '#6A9955',
            'number': '#B5CEA8',
            'function': '#DCDCAA',
            'class': '#4EC9B0',
            'builtin': '#C586C0',
            'operator': '#D4D4D4',
            'bracket': '#D4D4D4',
            'tag': '#569CD6',
            'attribute': '#92C5F8',
            'css_property': '#9CDCFE',
            'css_value': '#CE9178'
        },
        'monokai': {
            'keyword': '#F92672',
            'string': '#E6DB74',
            'comment': '#75715E',
            'number': '#AE81FF',
            'function': '#A6E22E',
            'class': '#66D9EF',
            'builtin': '#F92672',
            'operator': '#F8F8F2',
            'bracket': '#F8F8F2',
            'tag': '#F92672',
            'attribute': '#A6E22E',
            'css_property': '#66D9EF',
            'css_value': '#E6DB74'
        }
    }
    
    # Language extensions mapping
    LANGUAGE_EXTENSIONS = {
        '.py': 'python',
        '.pyw': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.txt': 'text',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.java': 'java',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.sql': 'sql'
    }
    
    # Keyboard shortcuts
    SHORTCUTS = {
        'new_tab': '<Control-t>',
        'close_tab': '<Control-w>',
        'save': '<Control-s>',
        'save_as': '<Control-Shift-s>',
        'open': '<Control-o>',
        'find': '<Control-f>',
        'replace': '<Control-h>',
        'goto_line': '<Control-g>',
        'select_all': '<Control-a>',
        'undo': '<Control-z>',
        'redo': '<Control-y>',
        'copy': '<Control-c>',
        'cut': '<Control-x>',
        'paste': '<Control-v>',
        'duplicate_line': '<Control-d>',
        'comment_toggle': '<Control-slash>',
        'zoom_in': '<Control-equal>',
        'zoom_out': '<Control-minus>',
        'toggle_sidebar': '<Control-b>',
        'toggle_terminal': '<Control-grave>',
        'new_file': '<Control-n>',
        'quit': '<Control-q>'
    }
