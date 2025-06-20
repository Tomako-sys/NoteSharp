# Petit utilitaire Python : Bloc-notes évolué (Windows, zéro dépendance)
# Numérotation des lignes + rechercher/remplacer (Ctrl+F)
# Menu Edition (couper, copier, coller, annuler, sélectionner tout)
# Raccourcis clavier classiques (Ctrl+S, Ctrl+O, Ctrl+Q, Ctrl+F, etc.)

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class MiniBlocNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Bloc-notes")
        self.root.geometry("700x520")

        # Conteneur principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)

        # Numérotation des lignes (à gauche)
        self.line_numbers = tk.Text(self.main_frame, width=4, padx=4, takefocus=0, border=0, background='#EEE', state='disabled', font=("Consolas", 12))
        self.line_numbers.pack(side='left', fill='y')

        # Zone texte principale
        self.text = tk.Text(self.main_frame, wrap='word', font=("Consolas", 12), undo=True)
        self.text.pack(side='right', fill='both', expand=True)

        # Synchroniser scroll
        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.sync_scroll)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

        # Menus
        menubar = tk.Menu(root)
        # Menu Fichier
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Ouvrir... (Ctrl+O)", command=self.ouvrir)
        filemenu.add_command(label="Enregistrer sous... (Ctrl+S)", command=self.enregistrer)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter (Ctrl+Q)", command=root.quit)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        # Menu Edition
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Annuler", command=lambda: self.text.event_generate('<<Undo>>'))
        editmenu.add_separator()
        editmenu.add_command(label="Couper", command=lambda: self.text.event_generate('<<Cut>>'))
        editmenu.add_command(label="Copier", command=lambda: self.text.event_generate('<<Copy>>'))
        editmenu.add_command(label="Coller", command=lambda: self.text.event_generate('<<Paste>>'))
        editmenu.add_separator()
        editmenu.add_command(label="Sélectionner tout", command=lambda: self.text.event_generate('<<SelectAll>>'))
        menubar.add_cascade(label="Edition", menu=editmenu)
        # Menu Recherche
        searchmenu = tk.Menu(menubar, tearoff=0)
        searchmenu.add_command(label="Rechercher/remplacer... (Ctrl+F)", command=self.ouvrir_rechercher)
        menubar.add_cascade(label="Outils", menu=searchmenu)
        root.config(menu=menubar)

        # Raccourcis clavier
        root.bind('<Control-s>', lambda e: self.enregistrer())
        root.bind('<Control-S>', lambda e: self.enregistrer())
        root.bind('<Control-o>', lambda e: self.ouvrir())
        root.bind('<Control-O>', lambda e: self.ouvrir())
        root.bind('<Control-q>', lambda e: root.quit())
        root.bind('<Control-Q>', lambda e: root.quit())
        root.bind('<Control-a>', lambda e: self.selectionner_tout(e))
        root.bind('<Control-A>', lambda e: self.selectionner_tout(e))
        root.bind('<Control-f>', lambda e: self.ouvrir_rechercher())
        root.bind('<Control-F>', lambda e: self.ouvrir_rechercher())

        # Mise à jour numéros de lignes
        self.text.bind('<KeyRelease>', lambda e: self.maj_lignes())
        self.text.bind('<ButtonRelease-1>', lambda e: self.maj_lignes())
        self.text.bind('<MouseWheel>', lambda e: self.sync_scrollbar(e))
        self.text.bind('<Configure>', lambda e: self.maj_lignes())
        self.text.bind('<<Change>>', lambda e: self.maj_lignes())
        self.text.bind('<FocusIn>', lambda e: self.maj_lignes())

        self.maj_lignes()

    def sync_scroll(self, *args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def sync_scrollbar(self, event):
        self.line_numbers.yview_moveto(self.text.yview()[0])
        return 'break'

    def maj_lignes(self):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        nb_lignes = int(self.text.index('end-1c').split('.')[0])
        lignes = '\n'.join(str(i) for i in range(1, nb_lignes + 1))
        self.line_numbers.insert(1.0, lignes)
        self.line_numbers.config(state='disabled')

    def ouvrir(self):
        chemin = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if chemin:
            try:
                with open(chemin, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, contenu)
                self.maj_lignes()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir : {e}")

    def enregistrer(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        if chemin:
            try:
                contenu = self.text.get(1.0, tk.END)
                with open(chemin, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                messagebox.showinfo("Succès", "Fichier enregistré !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer : {e}")

    def selectionner_tout(self, event=None):
        self.text.tag_add('sel', '1.0', 'end')
        return 'break'

    def ouvrir_rechercher(self):
        RechercherRemplacer(self.root, self.text)

class RechercherRemplacer:
    def __init__(self, root, text_widget):
        self.text = text_widget
        self.top = tk.Toplevel(root)
        self.top.title("Rechercher / Remplacer")
        self.top.geometry("340x120")
        self.top.transient(root)
        self.top.grab_set()

        tk.Label(self.top, text="Rechercher :").grid(row=0, column=0, sticky='e')
        self.entry_search = tk.Entry(self.top, width=25)
        self.entry_search.grid(row=0, column=1, padx=5, pady=4)
        tk.Button(self.top, text="Suivant", command=self.trouver).grid(row=0, column=2, padx=5)

        tk.Label(self.top, text="Remplacer par :").grid(row=1, column=0, sticky='e')
        self.entry_replace = tk.Entry(self.top, width=25)
        self.entry_replace.grid(row=1, column=1, padx=5)
        tk.Button(self.top, text="Remplacer", command=self.remplacer).grid(row=1, column=2, padx=5)

        tk.Button(self.top, text="Tout remplacer", command=self.remplacer_tout).grid(row=2, column=1, pady=7)

        self.idx = '1.0'

    def trouver(self):
        recherche = self.entry_search.get()
        if not recherche:
            return
        self.text.tag_remove('found', '1.0', tk.END)
        idx = self.text.search(recherche, self.idx, nocase=1, stopindex=tk.END)
        if idx:
            fin = f"{idx}+{len(recherche)}c"
            self.text.tag_add('found', idx, fin)
            self.text.tag_config('found', background='yellow')
            self.text.mark_set("insert", fin)
            self.text.see(idx)
            self.idx = fin
        else:
            messagebox.showinfo("Recherche", "Aucune occurrence suivante trouvée.")
            self.idx = '1.0'

    def remplacer(self):
        recherche = self.entry_search.get()
        remplacement = self.entry_replace.get()
        if not recherche:
            return
        idx = self.text.search(recherche, '1.0', nocase=1, stopindex=tk.END)
        if idx:
            fin = f"{idx}+{len(recherche)}c"
            self.text.delete(idx, fin)
            self.text.insert(idx, remplacement)
            self.text.tag_remove('found', '1.0', tk.END)

    def remplacer_tout(self):
        recherche = self.entry_search.get()
        remplacement = self.entry_replace.get()
        if not recherche:
            return
        idx = '1.0'
        n = 0
        while True:
            idx = self.text.search(recherche, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            fin = f"{idx}+{len(recherche)}c"
            self.text.delete(idx, fin)
            self.text.insert(idx, remplacement)
            idx = fin
            n += 1
        self.text.tag_remove('found', '1.0', tk.END)
        messagebox.showinfo("Remplacement", f"{n} occurrence(s) remplacée(s).")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniBlocNotes(root)
    root.mainloop()
