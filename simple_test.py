#!/usr/bin/env python3
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
