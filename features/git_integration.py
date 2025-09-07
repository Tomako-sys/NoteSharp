# Git integration for NoteSharp
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading
from ui.themes import theme_manager

class GitIntegration:
    """Basic Git integration features"""
    
    def __init__(self, parent, status_callback=None):
        self.parent = parent
        self.status_callback = status_callback
        self.current_repo = None
        self.git_status = {}
        
        # Check if current directory is a git repo
        self.check_git_repo()
    
    def check_git_repo(self):
        """Check if current directory is a git repository"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=os.getcwd(),
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.current_repo = os.getcwd()
                self.update_git_status()
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.current_repo = None
        return False
    
    def update_git_status(self):
        """Update git status information"""
        if not self.current_repo:
            return
        
        def get_status():
            try:
                # Get current branch
                branch_result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    cwd=self.current_repo,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
                
                # Get status
                status_result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=self.current_repo,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                status_lines = status_result.stdout.strip().split('\n') if status_result.returncode == 0 else []
                
                # Parse status
                modified = []
                added = []
                deleted = []
                untracked = []
                
                for line in status_lines:
                    if not line.strip():
                        continue
                    
                    status_code = line[:2]
                    filename = line[3:]
                    
                    if status_code.startswith('M'):
                        modified.append(filename)
                    elif status_code.startswith('A'):
                        added.append(filename)
                    elif status_code.startswith('D'):
                        deleted.append(filename)
                    elif status_code.startswith('??'):
                        untracked.append(filename)
                
                self.git_status = {
                    'branch': current_branch,
                    'modified': modified,
                    'added': added,
                    'deleted': deleted,
                    'untracked': untracked
                }
                
                # Update status callback
                if self.status_callback:
                    self.parent.after(0, lambda: self.status_callback(self.git_status))
            
            except Exception as e:
                print(f"Error getting git status: {e}")
        
        # Run in separate thread
        thread = threading.Thread(target=get_status, daemon=True)
        thread.start()
    
    def create_git_panel(self, parent_frame):
        """Create a git status panel"""
        colors = theme_manager.get_colors()
        
        git_frame = tk.LabelFrame(
            parent_frame,
            text="🔄 Git Status",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 9, 'bold')
        )
        git_frame.pack(fill='x', padx=5, pady=5)
        
        if not self.current_repo:
            no_repo_label = tk.Label(
                git_frame,
                text="Not a git repository",
                bg=colors['bg'],
                fg=colors['fg'],
                font=('Segoe UI', 9)
            )
            no_repo_label.pack(pady=5)
            return git_frame
        
        # Branch info
        self.branch_label = tk.Label(
            git_frame,
            text=f"Branch: {self.git_status.get('branch', 'unknown')}",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 9, 'bold')
        )
        self.branch_label.pack(anchor='w', padx=5, pady=2)
        
        # Status summary
        self.status_label = tk.Label(
            git_frame,
            text="",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 9)
        )
        self.status_label.pack(anchor='w', padx=5, pady=2)
        
        # Action buttons
        button_frame = tk.Frame(git_frame, bg=colors['bg'])
        button_frame.pack(fill='x', padx=5, pady=5)
        
        # Refresh button
        refresh_btn = theme_manager.create_styled_button(
            button_frame,
            "🔄 Refresh",
            command=self.update_git_status
        )
        refresh_btn.pack(side='left', padx=2)
        
        # Add all button
        add_all_btn = theme_manager.create_styled_button(
            button_frame,
            "➕ Add All",
            command=self.git_add_all
        )
        add_all_btn.pack(side='left', padx=2)
        
        # Commit button
        commit_btn = theme_manager.create_styled_button(
            button_frame,
            "💾 Commit",
            command=self.git_commit_dialog
        )
        commit_btn.pack(side='left', padx=2)
        
        # Pull button
        pull_btn = theme_manager.create_styled_button(
            button_frame,
            "⬇️ Pull",
            command=self.git_pull
        )
        pull_btn.pack(side='right', padx=2)
        
        # Push button
        push_btn = theme_manager.create_styled_button(
            button_frame,
            "⬆️ Push",
            command=self.git_push
        )
        push_btn.pack(side='right', padx=2)
        
        self.update_status_display()
        return git_frame
    
    def update_status_display(self):
        """Update the status display"""
        if not hasattr(self, 'status_label'):
            return
        
        status_text = ""
        if self.git_status.get('modified'):
            status_text += f"Modified: {len(self.git_status['modified'])} "
        if self.git_status.get('added'):
            status_text += f"Added: {len(self.git_status['added'])} "
        if self.git_status.get('deleted'):
            status_text += f"Deleted: {len(self.git_status['deleted'])} "
        if self.git_status.get('untracked'):
            status_text += f"Untracked: {len(self.git_status['untracked'])} "
        
        if not status_text:
            status_text = "Working directory clean"
        
        self.status_label.config(text=status_text)
        
        if hasattr(self, 'branch_label'):
            self.branch_label.config(text=f"Branch: {self.git_status.get('branch', 'unknown')}")
    
    def git_add_all(self):
        """Add all changes to staging"""
        if not self.current_repo:
            messagebox.showerror("Error", "Not in a git repository")
            return
        
        def add_all():
            try:
                result = subprocess.run(
                    ['git', 'add', '.'],
                    cwd=self.current_repo,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.parent.after(0, lambda: messagebox.showinfo("Success", "All changes added to staging"))
                    self.parent.after(0, self.update_git_status)
                else:
                    self.parent.after(0, lambda: messagebox.showerror("Error", f"Git add failed: {result.stderr}"))
            
            except Exception as e:
                self.parent.after(0, lambda err=e: messagebox.showerror("Error", f"Git add failed: {str(err)}"))
        
        thread = threading.Thread(target=add_all, daemon=True)
        thread.start()
    
    def git_commit_dialog(self):
        """Show commit dialog"""
        if not self.current_repo:
            messagebox.showerror("Error", "Not in a git repository")
            return
        
        # Create commit dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Git Commit")
        dialog.geometry("400x250")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        colors = theme_manager.get_colors()
        dialog.configure(bg=colors['bg'])
        
        # Commit message
        tk.Label(
            dialog,
            text="Commit Message:",
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor='w', padx=10, pady=5)
        
        message_text = tk.Text(
            dialog,
            height=8,
            bg=colors['bg'],
            fg=colors['fg'],
            font=('Consolas', 10)
        )
        message_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=colors['bg'])
        button_frame.pack(fill='x', padx=10, pady=5)
        
        def do_commit():
            message = message_text.get('1.0', 'end-1c').strip()
            if not message:
                messagebox.showerror("Error", "Please enter a commit message")
                return
            
            dialog.destroy()
            self.git_commit(message)
        
        commit_btn = theme_manager.create_styled_button(
            button_frame,
            "Commit",
            command=do_commit
        )
        commit_btn.pack(side='right', padx=5)
        
        cancel_btn = theme_manager.create_styled_button(
            button_frame,
            "Cancel",
            command=dialog.destroy
        )
        cancel_btn.pack(side='right')
        
        message_text.focus_set()
    
    def git_commit(self, message):
        """Commit changes with message"""
        if not self.current_repo:
            messagebox.showerror("Error", "Not in a git repository")
            return
        
        def commit():
            try:
                result = subprocess.run(
                    ['git', 'commit', '-m', message],
                    cwd=self.current_repo,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.parent.after(0, lambda: messagebox.showinfo("Success", "Changes committed successfully"))
                    self.parent.after(0, self.update_git_status)
                else:
                    self.parent.after(0, lambda: messagebox.showerror("Error", f"Git commit failed: {result.stderr}"))
            
            except Exception as e:
                self.parent.after(0, lambda err=e: messagebox.showerror("Error", f"Git commit failed: {str(err)}"))
        
        thread = threading.Thread(target=commit, daemon=True)
        thread.start()
    
    def git_pull(self):
        """Pull changes from remote"""
        if not self.current_repo:
            messagebox.showerror("Error", "Not in a git repository")
            return
        
        def pull():
            try:
                result = subprocess.run(
                    ['git', 'pull'],
                    cwd=self.current_repo,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    self.parent.after(0, lambda: messagebox.showinfo("Success", f"Pull completed:\n{result.stdout}"))
                    self.parent.after(0, self.update_git_status)
                else:
                    self.parent.after(0, lambda: messagebox.showerror("Error", f"Git pull failed: {result.stderr}"))
            
            except Exception as e:
                self.parent.after(0, lambda err=e: messagebox.showerror("Error", f"Git pull failed: {str(err)}"))
        
        thread = threading.Thread(target=pull, daemon=True)
        thread.start()
    
    def git_push(self):
        """Push changes to remote"""
        if not self.current_repo:
            messagebox.showerror("Error", "Not in a git repository")
            return
        
        def push():
            try:
                result = subprocess.run(
                    ['git', 'push'],
                    cwd=self.current_repo,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    self.parent.after(0, lambda: messagebox.showinfo("Success", "Push completed successfully"))
                    self.parent.after(0, self.update_git_status)
                else:
                    self.parent.after(0, lambda: messagebox.showerror("Error", f"Git push failed: {result.stderr}"))
            
            except Exception as e:
                self.parent.after(0, lambda: messagebox.showerror("Error", f"Git push failed: {str(e)}"))
        
        thread = threading.Thread(target=push, daemon=True)
        thread.start()
    
    def get_file_status(self, file_path):
        """Get git status for a specific file"""
        if not self.current_repo:
            return None
        
        rel_path = os.path.relpath(file_path, self.current_repo)
        
        if rel_path in self.git_status.get('modified', []):
            return 'modified'
        elif rel_path in self.git_status.get('added', []):
            return 'added'
        elif rel_path in self.git_status.get('deleted', []):
            return 'deleted'
        elif rel_path in self.git_status.get('untracked', []):
            return 'untracked'
        
        return 'clean'