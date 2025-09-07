#!/usr/bin/env python3
"""
NoteSharp Pro Troubleshooting Script
Diagnoses common issues and provides solutions
"""

import sys
import os
import platform

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ ERROR: Python 3.8+ required")
        print("   💡 Solution: Update Python to 3.8 or higher")
        return False
    else:
        print("   ✅ Python version OK")
        return True

def check_tkinter():
    """Check if tkinter is available"""
    print("\n🖥️  Checking GUI support (tkinter)...")
    try:
        import tkinter as tk
        print("   ✅ tkinter available")
        
        # Try creating a simple window
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the window
            root.destroy()
            print("   ✅ GUI display working")
            return True
        except Exception as e:
            print(f"   ❌ GUI display error: {e}")
            print("   💡 Solution: Ensure you have a display/desktop environment")
            return False
            
    except ImportError as e:
        print(f"   ❌ tkinter not available: {e}")
        print("   💡 Solutions:")
        
        if platform.system() == "Linux":
            print("      • Ubuntu/Debian: sudo apt-get install python3-tk")
            print("      • CentOS/RHEL: sudo yum install tkinter")
            print("      • Arch: sudo pacman -S tk")
        elif platform.system() == "Darwin":
            print("      • macOS: Install Python from python.org (includes tkinter)")
            print("      • Or with Homebrew: brew install python-tk")
        elif platform.system() == "Windows":
            print("      • Reinstall Python from python.org with 'tcl/tk' option checked")
        
        return False

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'NoteSharp_Pro.py',
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
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"   ❌ Missing files: {len(missing_files)}")
        for file in missing_files:
            print(f"      • {file}")
        print("   💡 Solution: Re-download all NoteSharp Pro files")
        return False
    else:
        print(f"   ✅ All {len(required_files)} files present")
        return True

def test_imports():
    """Test importing core modules"""
    print("\n📦 Testing module imports...")
    
    modules_to_test = [
        ('config', 'Configuration'),
        ('ui.themes', 'Theme management'),
        ('syntax.highlighter', 'Syntax highlighting'),
        ('core.editor', 'Text editor')
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            # Add current directory to path
            sys.path.insert(0, os.path.dirname(__file__))
            __import__(module_name)
            print(f"   ✅ {description} ({module_name})")
        except ImportError as e:
            print(f"   ❌ {description} ({module_name}): {e}")
            failed_imports.append((module_name, str(e)))
        except Exception as e:
            print(f"   ⚠️  {description} ({module_name}): {e}")
    
    if failed_imports:
        print(f"\n   💡 Import issues found:")
        for module, error in failed_imports:
            print(f"      • {module}: {error}")
        return False
    
    return True

def check_environment():
    """Check system environment"""
    print("\n🖥️  System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python executable: {sys.executable}")
    
    # Check if running in container/virtual environment
    if os.path.exists('/.dockerenv'):
        print("   📦 Running in Docker container")
        print("   ⚠️  GUI apps may not work in containers without X11 forwarding")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   🐍 Running in virtual environment")
    
    # Check display
    if 'DISPLAY' in os.environ:
        print(f"   🖥️  Display: {os.environ['DISPLAY']}")
    else:
        print("   ❌ No DISPLAY environment variable (Linux/macOS)")

def create_simple_test():
    """Create a simple test version"""
    print("\n🧪 Creating simple test version...")
    
    simple_code = '''#!/usr/bin/env python3
"""
Simple NoteSharp Test - Minimal version to verify tkinter works
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    def test_app():
        root = tk.Tk()
        root.title("NoteSharp Pro - Test Version")
        root.geometry("600x400")
        
        # Simple text editor
        text_area = tk.Text(root, wrap='word', font=('Consolas', 12))
        text_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status bar
        status = tk.Label(root, text="NoteSharp Pro Test - If you see this, GUI works!", 
                         anchor='w', relief='sunken')
        status.pack(side='bottom', fill='x')
        
        # Sample content
        text_area.insert('1.0', """# NoteSharp Pro Test

If you can see this window, the basic GUI is working!

Next steps:
1. Close this window
2. Try running: python NoteSharp_Pro.py
3. If that fails, check the troubleshooting output above

This is a simplified test to verify tkinter works on your system.
""")
        
        root.mainloop()
    
    if __name__ == "__main__":
        print("✅ tkinter working - launching test window...")
        test_app()
        
except ImportError as e:
    print(f"❌ tkinter not available: {e}")
    print("Please install tkinter for your system")
except Exception as e:
    print(f"❌ Error: {e}")
'''
    
    with open('simple_test.py', 'w') as f:
        f.write(simple_code)
    
    print("   ✅ Created simple_test.py")
    print("   💡 Run: python simple_test.py")

def provide_solutions():
    """Provide solutions based on system"""
    print("\n💡 SOLUTIONS & ALTERNATIVES:")
    
    system = platform.system()
    
    print("\n1️⃣ Fix tkinter (GUI support):")
    if system == "Linux":
        print("   sudo apt-get update && sudo apt-get install python3-tk")
        print("   # or for CentOS/RHEL: sudo yum install tkinter")
    elif system == "Darwin":
        print("   brew install python-tk")
        print("   # or reinstall Python from python.org")
    elif system == "Windows":
        print("   Reinstall Python from python.org with tkinter option checked")
    
    print("\n2️⃣ Run original version (simpler):")
    print("   python NoteSharp.pyw")
    
    print("\n3️⃣ Test with simple version:")
    print("   python simple_test.py")
    
    print("\n4️⃣ Run in proper environment:")
    print("   • Use local machine with desktop (not server/container)")
    print("   • Ensure you have GUI/desktop environment")
    print("   • For remote: Use X11 forwarding or VNC")
    
    print("\n5️⃣ Alternative text editors (if GUI fails):")
    print("   • nano: Simple terminal editor")
    print("   • vim: Advanced terminal editor") 
    print("   • code: VS Code (if available)")

def main():
    """Main troubleshooting function"""
    print("🔧 NoteSharp Pro Troubleshooting")
    print("=" * 50)
    
    issues_found = 0
    
    if not check_python_version():
        issues_found += 1
    
    if not check_tkinter():
        issues_found += 1
    
    if not check_file_structure():
        issues_found += 1
    
    if not test_imports():
        issues_found += 1
    
    check_environment()
    
    if issues_found == 0:
        print("\n🎉 All checks passed!")
        print("💡 Try running: python NoteSharp_Pro.py")
    else:
        print(f"\n⚠️  Found {issues_found} issues")
        create_simple_test()
        provide_solutions()
    
    print("\n" + "=" * 50)
    print("Need help? Check the solutions above! 👆")

if __name__ == "__main__":
    main()