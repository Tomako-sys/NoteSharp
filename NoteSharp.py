import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font
import keyword
import os
import re

class MiniBlocNotes:
    def __init__(self, root, on_tab_title_change=None):
        self.root = root
        self.file_path = None
        self.text_changed = False
        self.font_family = "Consolas"
        self.font_size = 12
        self.theme = "light"
        self.on_tab_title_change = on_tab_title_change  # callback pour changer le nom d'onglet
        self._auto_save_job = None

        # Frame principale
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)
        # Numérotation des lignes (à gauche)
        self.line_numbers = tk.Text(self.main_frame, width=4, padx=4, takefocus=0, border=0, background='#EEE', state='disabled', font=(self.font_family, self.font_size))
        self.line_numbers.pack(side='left', fill='y')
        # Zone texte principale
        self.text = tk.Text(self.main_frame, wrap='word', font=(self.font_family, self.font_size), undo=True)
        self.text.pack(side='right', fill='both', expand=True)
        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.sync_scroll)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        # Barre de statut
        self.status = tk.Label(root, text="Caractères : 0 | Mots : 0 | Lignes : 0 | Parags : 0 | Sélection : 0", anchor='w')
        self.status.pack(side='bottom', fill='x')

        # Bindings
        self.text.bind('<KeyRelease>', self.on_change)
        self.text.bind('<ButtonRelease-1>', lambda e: self.maj_lignes())
        self.text.bind('<MouseWheel>', lambda e: self.sync_scrollbar(e))
        self.text.bind('<Configure>', lambda e: self.maj_lignes())
        self.text.bind('<<Selection>>', lambda e: self.maj_statut())
        self.text.bind('<ButtonRelease-1>', lambda e: self.maj_statut())
        self.text.bind('<KeyRelease>', lambda e: self.maj_statut())
        self.text.bind('<KeyRelease>', self.coloration_syntaxique)
        self.maj_lignes()
        self.maj_statut()

    # Fonctions scroll & lignes
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
    # Statut en bas
    def maj_statut(self):
        contenu = self.text.get(1.0, tk.END)
        nb_car = len(contenu.rstrip('\n'))
        nb_lignes = int(self.text.index('end-1c').split('.')[0])
        mots = len(contenu.split())
        parags = contenu.count('\n\n') + 1
        try:
            sel = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            nb_sel = len(sel)
        except:
            nb_sel = 0
        self.status.config(
            text=f"Caractères : {nb_car} | Mots : {mots} | Lignes : {nb_lignes} | Parags : {parags} | Sélection : {nb_sel}"
        )
    # Détection modification
    def on_change(self, event=None):
        self.maj_lignes()
        self.maj_statut()
        self.text_changed = True
        self.coloration_syntaxique()
    # Gestion fichiers
    def ouvrir(self):
        if self.text_changed and not self.demande_sauvegarde():
            return
        chemin = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Python (*.py)", "*.py"), ("Tous", "*.*")])
        if chemin:
            try:
                with open(chemin, 'r', encoding='utf-8') as f:
                    contenu = f.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, contenu)
                self.file_path = chemin
                if self.on_tab_title_change:
                    self.on_tab_title_change(os.path.basename(chemin))
                self.text_changed = False
                self.maj_lignes()
                self.maj_statut()
                self.coloration_syntaxique()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir : {e}")
    def enregistrer(self):
        if self.file_path:
            try:
                contenu = self.text.get(1.0, tk.END)
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                messagebox.showinfo("Succès", "Fichier enregistré !")
                self.text_changed = False
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer : {e}")
        else:
            self.enregistrer_sous()
    def enregistrer_sous(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Python (*.py)", "*.py"), ("Tous", "*.*")])
        if chemin:
            try:
                contenu = self.text.get(1.0, tk.END)
                with open(chemin, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                self.file_path = chemin
                if self.on_tab_title_change:
                    self.on_tab_title_change(os.path.basename(chemin))
                messagebox.showinfo("Succès", "Fichier enregistré !")
                self.text_changed = False
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer : {e}")
    def demande_sauvegarde(self):
        rep = messagebox.askyesnocancel("Enregistrer les modifications ?", "Voulez-vous enregistrer les modifications avant de continuer ?")
        if rep is None:
            return False # Annulé
        if rep:
            self.enregistrer()
            return True
        return True
    def demande_fermeture(self):
        if self.text_changed and not self.demande_sauvegarde():
            return
        self.root.destroy()
    def selectionner_tout(self, event=None):
        self.text.tag_add('sel', '1.0', 'end')
        return 'break'
    # Recherche/remplacement
    def ouvrir_rechercher(self):
        RechercherRemplacer(self.root, self.text)
    # Police & thèmes
    def changer_police(self):
        familles = list(font.families())
        famille = simpledialog.askstring("Police", "Nom de la police :\n(ex : Consolas, Courier, Arial)", initialvalue=self.font_family)
        if famille and famille in familles:
            self.font_family = famille
            self.text.config(font=(self.font_family, self.font_size))
            self.line_numbers.config(font=(self.font_family, self.font_size))
    def changer_taille(self):
        taille = simpledialog.askinteger("Taille de police", "Nouvelle taille :", initialvalue=self.font_size, minvalue=6, maxvalue=72)
        if taille:
            self.font_size = taille
            self.text.config(font=(self.font_family, self.font_size))
            self.line_numbers.config(font=(self.font_family, self.font_size))
    def toggle_theme(self):
        if self.theme == "light":
            bg, fg, lbg = '#232629', '#FFFFFF', '#181a1b'
            self.theme = "dark"
        else:
            bg, fg, lbg = '#FFFFFF', '#000000', '#EEE'
            self.theme = "light"
        self.text.config(bg=bg, fg=fg, insertbackground=fg)
        self.line_numbers.config(bg=lbg, fg=fg)
        self.status.config(bg=lbg, fg=fg)

    # --------- OUTILS ---------
    def demarrer_auto_save(self, interval_sec=120):
        self.stopper_auto_save()
        def auto_save():
            if self.file_path:
                contenu = self.text.get(1.0, tk.END)
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
            self._auto_save_job = self.text.after(interval_sec*1000, auto_save)
        auto_save()
        messagebox.showinfo("Auto-save", "Sauvegarde auto activée (toutes les 2 min).")
    def stopper_auto_save(self):
        if self._auto_save_job:
            self.text.after_cancel(self._auto_save_job)
            self._auto_save_job = None
            messagebox.showinfo("Auto-save", "Sauvegarde auto désactivée.")
    def set_lecture_seule(self, etat=True):
        self.text.config(state=tk.DISABLED if etat else tk.NORMAL)
        messagebox.showinfo("Lecture seule", "Lecture seule activée." if etat else "Mode édition activé.")
    def inserer_snippet(self, nom):
        snippets = {
            "Entête": "# Titre du document\n\n",
            "Signature": "\n\nCordialement,\nVotre nom\n",
            "Date": "Date : __/__/____\n",
        }
        self.text.insert(tk.INSERT, snippets.get(nom, ""))
    def coloration_html_css(self, event=None):
        self.text.tag_remove("htmltag", "1.0", tk.END)
        for m in re.finditer(r'<[^>]+>', self.text.get(1.0, tk.END)):
            start = "1.0 + %dc" % m.start()
            end = "1.0 + %dc" % m.end()
            self.text.tag_add("htmltag", start, end)
        self.text.tag_config("htmltag", foreground="darkred")
        self.text.tag_remove("csstag", "1.0", tk.END)
        for m in re.finditer(r'\.[\w\-]+\s*{', self.text.get(1.0, tk.END)):
            start = "1.0 + %dc" % m.start()
            end = "1.0 + %dc" % m.end()
            self.text.tag_add("csstag", start, end)
        self.text.tag_config("csstag", foreground="darkblue")
    # Coloration syntaxique Python
    def coloration_syntaxique(self, event=None):
        self.text.tag_remove("pykeyword", "1.0", tk.END)
        for mot in keyword.kwlist:
            start = "1.0"
            while True:
                pos = self.text.search(r'\b' + mot + r'\b', start, stopindex=tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(mot)}c"
                self.text.tag_add("pykeyword", pos, end)
                start = end
        self.text.tag_config("pykeyword", foreground="blue", font=(self.font_family, self.font_size, "bold"))

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

class BlocNotesOnglets:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteSharp avec Onglets")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        self.onglets = []

        # Menus
        menubar = tk.Menu(root)
        # Menu Fichier
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nouvel onglet", command=self.ajouter_onglet)
        filemenu.add_command(label="Ouvrir... (Ctrl+O)", command=lambda: self.onglet_courant().ouvrir())
        filemenu.add_command(label="Enregistrer (Ctrl+S)", command=lambda: self.onglet_courant().enregistrer())
        filemenu.add_command(label="Enregistrer sous...", command=lambda: self.onglet_courant().enregistrer_sous())
        filemenu.add_separator()
        filemenu.add_command(label="Fermer l'onglet", command=self.fermer_onglet)
        filemenu.add_command(label="Quitter (Ctrl+Q)", command=self.demande_fermeture)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        # Menu Edition
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Annuler", command=lambda: self.onglet_courant().text.event_generate('<<Undo>>'))
        editmenu.add_separator()
        editmenu.add_command(label="Couper", command=lambda: self.onglet_courant().text.event_generate('<<Cut>>'))
        editmenu.add_command(label="Copier", command=lambda: self.onglet_courant().text.event_generate('<<Copy>>'))
        editmenu.add_command(label="Coller", command=lambda: self.onglet_courant().text.event_generate('<<Paste>>'))
        editmenu.add_separator()
        editmenu.add_command(label="Sélectionner tout", command=lambda: self.onglet_courant().selectionner_tout())
        menubar.add_cascade(label="Edition", menu=editmenu)
        # Menu Outils
        searchmenu = tk.Menu(menubar, tearoff=0)
        searchmenu.add_command(label="Rechercher/remplacer... (Ctrl+F)", command=lambda: self.onglet_courant().ouvrir_rechercher())
        searchmenu.add_command(label="Activer sauvegarde auto", command=lambda: self.onglet_courant().demarrer_auto_save())
        searchmenu.add_command(label="Désactiver sauvegarde auto", command=lambda: self.onglet_courant().stopper_auto_save())
        searchmenu.add_command(label="Recherche tous les onglets", command=self.rechercher_tous_onglets)
        searchmenu.add_command(label="Activer lecture seule", command=lambda: self.onglet_courant().set_lecture_seule(True))
        searchmenu.add_command(label="Désactiver lecture seule", command=lambda: self.onglet_courant().set_lecture_seule(False))
        # Snippets sous-menu
        snipmenu = tk.Menu(searchmenu, tearoff=0)
        for nom in ["Entête", "Signature", "Date"]:
            snipmenu.add_command(label=nom, command=lambda n=nom: self.onglet_courant().inserer_snippet(n))
        searchmenu.add_cascade(label="Insérer un snippet", menu=snipmenu)
        searchmenu.add_command(label="Coloration HTML/CSS", command=lambda: self.onglet_courant().coloration_html_css())
        menubar.add_cascade(label="Outils", menu=searchmenu)
        # Menu Affichage
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Police...", command=lambda: self.onglet_courant().changer_police())
        viewmenu.add_command(label="Taille de police...", command=lambda: self.onglet_courant().changer_taille())
        viewmenu.add_separator()
        viewmenu.add_command(label="Mode nuit/jour", command=lambda: self.onglet_courant().toggle_theme())
        menubar.add_cascade(label="Affichage", menu=viewmenu)
        root.config(menu=menubar)

        # Raccourcis clavier
        root.bind('<Control-s>', lambda e: self.onglet_courant().enregistrer())
        root.bind('<Control-S>', lambda e: self.onglet_courant().enregistrer())
        root.bind('<Control-o>', lambda e: self.onglet_courant().ouvrir())
        root.bind('<Control-O>', lambda e: self.onglet_courant().ouvrir())
        root.bind('<Control-q>', lambda e: self.demande_fermeture())
        root.bind('<Control-Q>', lambda e: self.demande_fermeture())
        root.bind('<Control-a>', lambda e: self.onglet_courant().selectionner_tout())
        root.bind('<Control-A>', lambda e: self.onglet_courant().selectionner_tout())
        root.bind('<Control-f>', lambda e: self.onglet_courant().ouvrir_rechercher())
        root.bind('<Control-F>', lambda e: self.onglet_courant().ouvrir_rechercher())
        root.protocol("WM_DELETE_WINDOW", self.demande_fermeture)

        self.ajouter_onglet()

    def ajouter_onglet(self):
        frame = tk.Frame(self.notebook)
        def maj_nom_onglet(nom):
            self.notebook.tab(frame, text=nom)
        editeur = MiniBlocNotes(frame, on_tab_title_change=maj_nom_onglet)
        self.notebook.add(frame, text="Nouveau")
        self.onglets.append(editeur)
        self.notebook.select(len(self.onglets)-1)
        return editeur

    def fermer_onglet(self):
        if len(self.onglets) <= 1:
            messagebox.showinfo("Onglet", "Impossible de fermer le dernier onglet.")
            return
        idx = self.notebook.index(self.notebook.select())
        self.notebook.forget(idx)
        del self.onglets[idx]

    def demande_fermeture(self):
        for onglet in self.onglets:
            if onglet.text_changed:
                self.root.lift()
                if not onglet.demande_sauvegarde():
                    return
        self.root.destroy()

    def onglet_courant(self):
        idx = self.notebook.index(self.notebook.select())
        return self.onglets[idx]

    def rechercher_tous_onglets(self):
        terme = simpledialog.askstring("Recherche globale", "Mot à chercher :")
        if not terme:
            return
        resultats = []
        for idx, ong in enumerate(self.onglets):
            contenu = ong.text.get(1.0, tk.END)
            lignes = contenu.splitlines()
            for num, ligne in enumerate(lignes, 1):
                if terme in ligne:
                    resultats.append(f"Onglet {idx+1}, ligne {num} : {ligne.strip()}")
        if resultats:
            messagebox.showinfo("Résultats", "\n".join(resultats[:20]) + (f"\n...({len(resultats)-20} de plus)" if len(resultats) > 20 else ""))
        else:
            messagebox.showinfo("Résultats", "Aucune occurrence trouvée.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlocNotesOnglets(root)
    root.mainloop()
