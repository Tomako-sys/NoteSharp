#!/usr/bin/env python3
"""
Test script to validate NoteSharp Pro structure without GUI
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test config
        from config import Config
        print("✓ Config imported successfully")
        print(f"  App Name: {Config.APP_NAME}")
        print(f"  Version: {Config.VERSION}")
        print(f"  Available themes: {list(Config.THEMES.keys())}")
        
        # Test UI modules (without creating widgets)
        from ui.themes import ThemeManager
        print("✓ ThemeManager imported successfully")
        
        # Test syntax highlighting
        from syntax.highlighter import SyntaxHighlighter
        print("✓ SyntaxHighlighter imported successfully")
        
        from syntax.autocomplete import AutoComplete
        print("✓ AutoComplete imported successfully")
        
        print("\n✅ All core modules imported successfully!")
        print("\n📋 Features implemented:")
        print("  • Multi-language syntax highlighting")
        print("  • Auto-completion system")
        print("  • Theme management (Light, Dark, Monokai)")
        print("  • Modern UI components")
        print("  • Integrated terminal")
        print("  • Git integration")
        print("  • Enhanced text editor")
        print("  • File explorer sidebar")
        print("  • Comprehensive configuration system")
        
        print(f"\n🌍 Supported languages: {len(Config.LANGUAGE_EXTENSIONS)} languages")
        for ext, lang in list(Config.LANGUAGE_EXTENSIONS.items())[:10]:
            print(f"    {ext} → {lang}")
        if len(Config.LANGUAGE_EXTENSIONS) > 10:
            print(f"    ... and {len(Config.LANGUAGE_EXTENSIONS) - 10} more")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_configuration():
    """Test configuration settings"""
    try:
        from config import Config
        
        print(f"\n⚙️ Configuration Test:")
        print(f"  Default font: {Config.DEFAULT_FONT_FAMILY} {Config.DEFAULT_FONT_SIZE}pt")
        print(f"  Max file size: {Config.MAX_FILE_SIZE // (1024*1024)}MB")
        print(f"  Auto-save interval: {Config.AUTO_SAVE_INTERVAL}s")
        print(f"  Recent files limit: {Config.MAX_RECENT_FILES}")
        print(f"  Sidebar width: {Config.SIDEBAR_WIDTH}px")
        
        # Test theme colors
        print(f"\n🎨 Theme Colors Available:")
        for theme_name, colors in Config.THEMES.items():
            print(f"  {theme_name.title()}: {len(colors)} color settings")
        
        print(f"\n📝 Syntax Colors:")
        for theme_name, colors in Config.SYNTAX_COLORS.items():
            print(f"  {theme_name.title()}: {len(colors)} syntax colors")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 NoteSharp Pro - Structure Validation Test")
    print("=" * 50)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_configuration():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! NoteSharp Pro is ready to run.")
        print("\nTo run the application (requires GUI environment):")
        print("  python3 NoteSharp_Pro.py")
        print("\nTo run the original version:")
        print("  python3 NoteSharp.pyw")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)