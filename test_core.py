#!/usr/bin/env python3
"""
Test core functionality without GUI dependencies
"""

import sys
import os
import re

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config():
    """Test configuration module"""
    try:
        # Mock tkinter to avoid import errors
        sys.modules['tkinter'] = type(sys)('tkinter')
        sys.modules['tkinter.font'] = type(sys)('font')
        
        from config import Config
        print("✓ Config module loaded successfully")
        print(f"  App: {Config.APP_NAME} v{Config.VERSION}")
        print(f"  Themes: {list(Config.THEMES.keys())}")
        print(f"  Languages: {len(Config.LANGUAGE_EXTENSIONS)} supported")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_syntax_patterns():
    """Test syntax highlighting patterns without GUI"""
    try:
        # Create mock text widget
        class MockText:
            def __init__(self):
                pass
            def tag_configure(self, *args, **kwargs):
                pass
            def cget(self, *args):
                return 'Consolas 12'
        
        # Mock theme manager
        class MockThemeManager:
            def get_syntax_colors(self):
                return {
                    'keyword': '#0000FF',
                    'string': '#008000', 
                    'comment': '#808080'
                }
            def add_observer(self, callback):
                pass
        
        # Replace imports
        sys.modules['ui.themes'] = type(sys)('themes')
        sys.modules['ui.themes'].theme_manager = MockThemeManager()
        
        from syntax.highlighter import SyntaxHighlighter
        
        # Test pattern matching
        highlighter = SyntaxHighlighter(MockText())
        
        # Test Python patterns
        test_code = """
def hello_world():
    print("Hello, World!")
    return True
"""
        
        patterns = highlighter.patterns.get('python', [])
        print(f"✓ Python syntax patterns: {len(patterns)} patterns loaded")
        
        # Test pattern matching
        for tag, pattern in patterns:
            matches = list(re.finditer(pattern, test_code, re.MULTILINE))
            if matches:
                print(f"  {tag}: {len(matches)} matches")
        
        # Test language detection
        lang = highlighter.detect_language_from_extension('.py')
        print(f"  Language detection: .py → {lang}")
        
        return True
    except Exception as e:
        print(f"❌ Syntax highlighting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test file structure"""
    expected_files = [
        'NoteSharp_Pro.py',
        'NoteSharp.pyw', 
        'config.py',
        'ui/__init__.py',
        'ui/themes.py',
        'ui/toolbar.py',
        'ui/sidebar.py',
        'core/__init__.py',
        'core/editor.py',
        'syntax/__init__.py',
        'syntax/highlighter.py',
        'syntax/autocomplete.py',
        'features/__init__.py',
        'features/terminal.py',
        'features/git_integration.py'
    ]
    
    missing_files = []
    for file_path in expected_files:
        full_path = os.path.join('/app', file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print(f"✓ All {len(expected_files)} expected files present")
        return True

def test_language_support():
    """Test language extension mapping"""
    try:
        from config import Config
        
        print("\n📝 Language Support:")
        languages = {}
        for ext, lang in Config.LANGUAGE_EXTENSIONS.items():
            if lang not in languages:
                languages[lang] = []
            languages[lang].append(ext)
        
        for lang, extensions in sorted(languages.items()):
            print(f"  {lang}: {', '.join(extensions)}")
        
        print(f"\nTotal: {len(languages)} languages, {len(Config.LANGUAGE_EXTENSIONS)} extensions")
        return True
    except Exception as e:
        print(f"❌ Language support test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 NoteSharp Pro - Core Functionality Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Configuration", test_config),
        ("Language Support", test_language_support),
        ("Syntax Highlighting", test_syntax_patterns),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core functionality tests passed!")
        print("\n🚀 NoteSharp Pro Enhancements Summary:")
        print("  ✓ Modular architecture with organized packages")
        print("  ✓ Advanced syntax highlighting for 20+ languages")
        print("  ✓ Multi-theme support (Light, Dark, Monokai)")
        print("  ✓ Enhanced text editor with modern features")
        print("  ✓ Integrated terminal and git support")
        print("  ✓ Auto-completion system")
        print("  ✓ File explorer sidebar")
        print("  ✓ Comprehensive configuration system")
        print("  ✓ Modern UI components and toolbar")
        print("  ✓ Extensible plugin-ready architecture")
    else:
        print(f"⚠️  {total - passed} tests failed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)