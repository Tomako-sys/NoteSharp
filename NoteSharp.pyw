import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font
from datetime import datetime
import keyword
import os
import re

LANG = {
    'en': {
        'file': "File",
        'new_tab': "New Tab",
        'open': "Open... (Ctrl+O)",
        'save': "Save (Ctrl+S)",
        'saveas': "Save As...",
        'close_tab': "Close Tab",
        'quit': "Quit (Ctrl+Q)",
        'recent': "Recent",
        'edit': "Edit",
        'undo': "Undo",
        'cut': "Cut",
        'copy': "Copy",
        'paste': "Paste",
        'select_all': "Select All",
        'tools': "Tools",
        'find_replace': "Find/Replace... (Ctrl+F)",
        'auto_save_on': "Enable Auto-save",
        'auto_save_off': "Disable Auto-save",
        'global_search': "Global Search",
        'readonly_on': "Enable Read-Only",
        'readonly_off': "Disable Read-Only",
        'snippets': "Insert Snippet",
        'snippet_header': "Header",
        'snippet_signature': "Signature",
        'snippet_date': "Date",
        'color_html': "HTML/CSS Highlight",
        'word_wrap': "Toggle Word Wrap",
        'lock_tab': "Lock Tab",
        'unlock_tab': "Unlock Tab",
        'goto_line': "Go to Line",
        'upper': "To UPPERCASE",
        'lower': "To lowercase",
        'duplicate_line': "Duplicate Line",
        'show_invisibles': "Show Invisibles",
        'insert_timestamp': "Insert Timestamp",
        'view': "View",
        'font': "Font...",
        'fontsize': "Font Size...",
        'theme': "Dark/Light Mode",
        'language': "Language",
        'tab_new': "New",
        'tab_locked': "🔒",
        # dialogs/messages:
        'save_changes': "Save changes before continuing?",
        'success': "Success",
        'file_saved': "File saved!",
        'cannot_open': "Cannot open file:",
        'cannot_save': "Cannot save file:",
        'cannot_close_last_tab': "Cannot close the last tab.",
        'tab_locked_msg': "This tab is locked!",
        'tab_locked_info': "Tab locked!",
        'tab_unlocked_info': "Tab unlocked.",
        'results': "Results",
        'none_found': "No matches found.",
        'recovery_found': "Auto-saved version found. Load?",
        'status': "Characters: {chars} | Words: {words} | Lines: {lines} | Paragraphs: {parags} | Selection: {sel}"
    },
    'fr': {
        'file': "Fichier",
        'new_tab': "Nouvel onglet",
        'open': "Ouvrir... (Ctrl+O)",
        'save': "Enregistrer (Ctrl+S)",
        'saveas': "Enregistrer sous...",
        'close_tab': "Fermer l'onglet",
        'quit': "Quitter (Ctrl+Q)",
        'recent': "Récents",
        'edit': "Edition",
        'undo': "Annuler",
        'cut': "Couper",
        'copy': "Copier",
        'paste': "Coller",
        'select_all': "Sélectionner tout",
        'tools': "Outils",
        'find_replace': "Rechercher/remplacer... (Ctrl+F)",
        'auto_save_on': "Activer sauvegarde auto",
        'auto_save_off': "Désactiver sauvegarde auto",
        'global_search': "Recherche tous les onglets",
        'readonly_on': "Activer lecture seule",
        'readonly_off': "Désactiver lecture seule",
        'snippets': "Insérer un snippet",
        'snippet_header': "Entête",
        'snippet_signature': "Signature",
        'snippet_date': "Date",
        'color_html': "Coloration HTML/CSS",
        'word_wrap': "Activer/désactiver retour à la ligne",
        'lock_tab': "Verrouiller l'onglet",
        'unlock_tab': "Déverrouiller l'onglet",
        'goto_line': "Aller à la ligne",
        'upper': "En MAJUSCULES",
        'lower': "En minuscules",
        'duplicate_line': "Dupliquer la ligne",
        'show_invisibles': "Afficher les invisibles",
        'insert_timestamp': "Insérer l'horodatage",
        'view': "Affichage",
        'font': "Police...",
        'fontsize': "Taille de police...",
        'theme': "Mode nuit/jour",
        'language': "Langue",
        'tab_new': "Nouveau",
        'tab_locked': "🔒",
        # dialogs/messages:
        'save_changes': "Voulez-vous enregistrer les modifications avant de continuer ?",
        'success': "Succès",
        'file_saved': "Fichier enregistré !",
        'cannot_open': "Impossible d'ouvrir :",
        'cannot_save': "Impossible d'enregistrer :",
        'cannot_close_last_tab': "Impossible de fermer le dernier onglet.",
        'tab_locked_msg': "Cet onglet est verrouillé !",
        'tab_locked_info': "Onglet verrouillé !",
        'tab_unlocked_info': "Onglet déverrouillé.",
        'results': "Résultats",
        'none_found': "Aucune occurrence trouvée.",
        'recovery_found': "Version auto-sauvegardée trouvée. Charger ?",
        'status': "Caractères : {chars} | Mots : {words} | Lignes : {lines} | Parags : {parags} | Sélection : {sel}"
    }
}

class MiniBlocNotes:
    def __init__(self, root, lang_getter, on_tab_title_change=None):
        self.root = root
        self.file_path = None
        self.text_changed = False
        self.font_family = "Consolas"
        self.font_size = 12
        self.theme = "light"
        self._auto_save_job = None
        self.on_tab_title_change = on_tab_title_change
        self.lang_getter = lang_getter
        self.locked = False
        self.wrap_mode = 'word'

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)
        self.line_numbers = tk.Text(self.main_frame, width=4, padx=4, takefocus=0, border=0, background='#EEE', state='disabled', font=(self.font_family, self.font_size))
        self.line_numbers.pack(side='left', fill='y')
        self.text = tk.Text(self.main_frame, wrap=self.wrap_mode, font=(self.font_family, self.font_size), undo=True)
        self.text.pack(side='right', fill='both', expand=True)
        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.sync_scroll)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        self.status = tk.Label(root, text="", anchor='w')
        self.status.pack(side='bottom', fill='x')

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

    def get_lang(self):
        return self.lang_getter()

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
    def maj_statut(self):
        L = LANG[self.get_lang()]
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
            text=L['status'].format(
                chars=nb_car, words=mots, lines=nb_lignes, parags=parags, sel=nb_sel
            )
        )
    def on_change(self, event=None):
        self.maj_lignes()
        self.maj_statut()
        self.text_changed = True
        self.coloration_syntaxique()
    def ouvrir(self):
        L = LANG[self.get_lang()]
        if self.text_changed and not self.demande_sauvegarde():
            return
        chemin = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Python (*.py)", "*.py"), ("All", "*.*")])
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
                if hasattr(self.root.master, 'add_to_recents'):
                    self.root.master.add_to_recents(chemin)
            except Exception as e:
                messagebox.showerror(L['cannot_open'], f"{chemin}\n{e}")
    def enregistrer(self):
        L = LANG[self.get_lang()]
        if self.file_path:
            try:
                contenu = self.text.get(1.0, tk.END)
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                messagebox.showinfo(L['success'], L['file_saved'])
                self.text_changed = False
                if hasattr(self.root.master, 'add_to_recents'):
                    self.root.master.add_to_recents(self.file_path)
            except Exception as e:
                messagebox.showerror(L['cannot_save'], f"{self.file_path}\n{e}")
        else:
            self.enregistrer_sous()
    def enregistrer_sous(self):
        L = LANG[self.get_lang()]
        chemin = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Python (*.py)", "*.py"), ("All", "*.*")])
        if chemin:
            try:
                contenu = self.text.get(1.0, tk.END)
                with open(chemin, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                self.file_path = chemin
                if self.on_tab_title_change:
                    self.on_tab_title_change(os.path.basename(chemin))
                messagebox.showinfo(L['success'], L['file_saved'])
                self.text_changed = False
                if hasattr(self.root.master, 'add_to_recents'):
                    self.root.master.add_to_recents(chemin)
            except Exception as e:
                messagebox.showerror(L['cannot_save'], f"{chemin}\n{e}")
    def demande_sauvegarde(self):
        L = LANG[self.get_lang()]
        rep = messagebox.askyesnocancel(L['save_changes'])
        if rep is None:
            return False
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
    def ouvrir_rechercher(self):
        RechercherRemplacer(self.root, self.text, self.get_lang)
    def changer_police(self):
        familles = list(font.families())
        famille = simpledialog.askstring("Font / Police", "Font name (e.g. Consolas, Courier, Arial):", initialvalue=self.font_family)
        if famille and famille in familles:
            self.font_family = famille
            self.text.config(font=(self.font_family, self.font_size))
            self.line_numbers.config(font=(self.font_family, self.font_size))
    def changer_taille(self):
        taille = simpledialog.askinteger("Font Size / Taille", "New font size:", initialvalue=self.font_size, minvalue=6, maxvalue=72)
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
    def demarrer_auto_save(self, interval_sec=120):
        self.stopper_auto_save()
        L = LANG[self.get_lang()]
        def auto_save():
            if self.file_path:
                contenu = self.text.get(1.0, tk.END)
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(contenu)
            self._auto_save_job = self.text.after(interval_sec*1000, auto_save)
        auto_save()
        messagebox.showinfo("Auto-save", (L['auto_save_on'] + " (2min)" if self.get_lang() == 'en' else "Sauvegarde auto activée (2 min)"))
    def stopper_auto_save(self):
        if self._auto_save_job:
            self.text.after_cancel(self._auto_save_job)
            self._auto_save_job = None
            L = LANG[self.get_lang()]
            messagebox.showinfo("Auto-save", L['auto_save_off'])
    def set_lecture_seule(self, etat=True):
        self.text.config(state=tk.DISABLED if etat else tk.NORMAL)
        L = LANG[self.get_lang()]
        messagebox.showinfo("Read-only / Lecture seule", L['readonly_on'] if etat else L['readonly_off'])
    def inserer_snippet(self, nom):
        snippets = {
            LANG['en']['snippet_header']: "# Document Title\n\n",
            LANG['en']['snippet_signature']: "\n\nBest regards,\nYour Name\n",
            LANG['en']['snippet_date']: "Date: __/__/____\n",
            LANG['fr']['snippet_header']: "# Titre du document\n\n",
            LANG['fr']['snippet_signature']: "\n\nCordialement,\nVotre nom\n",
            LANG['fr']['snippet_date']: "Date : __/__/____\n",
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

    # --- EXTRA TOOLS ---

    def toggle_word_wrap(self):
        self.wrap_mode = 'none' if self.text.cget('wrap') == 'word' else 'word'
        self.text.config(wrap=self.wrap_mode)

    def lock_tab(self, val=True):
        self.locked = val
        L = LANG[self.get_lang()]
        if self.on_tab_title_change:
            name = os.path.basename(self.file_path) if self.file_path else L['tab_new']
            if val and LANG[self.get_lang()]['tab_locked'] not in name:
                name += " " + LANG[self.get_lang()]['tab_locked']
            elif not val:
                name = name.replace(" " + LANG[self.get_lang()]['tab_locked'], "")
            self.on_tab_title_change(name)
        messagebox.showinfo("Tab Lock", L['tab_locked_info'] if val else L['tab_unlocked_info'])

    def go_to_line(self):
        L = LANG[self.get_lang()]
        num = simpledialog.askinteger(L['goto_line'], L['goto_line'] + " :")
        if num:
            index = f"{num}.0"
            self.text.mark_set(tk.INSERT, index)
            self.text.see(index)
            self.text.focus_set()

    def to_upper(self):
        try:
            sel = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text.insert(tk.INSERT, sel.upper())
        except:
            pass
    def to_lower(self):
        try:
            sel = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text.insert(tk.INSERT, sel.lower())
        except:
            pass

    def duplicate_line(self):
        index = self.text.index(tk.INSERT)
        line_num = int(index.split('.')[0])
        line_start = f"{line_num}.0"
        line_end = f"{line_num}.end"
        line_text = self.text.get(line_start, line_end) + "\n"
        self.text.insert(line_end, "\n" + line_text)

    def show_invisibles(self):
        content = self.text.get(1.0, tk.END)
        show = content.replace(' ', '·').replace('\t', '→')
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, show)

    def insert_timestamp(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text.insert(tk.INSERT, now)

class RechercherRemplacer:
    def __init__(self, root, text_widget, lang_getter):
        self.text = text_widget
        self.get_lang = lang_getter
        L = LANG[self.get_lang()]
        self.top = tk.Toplevel(root)
        self.top.title(L['find_replace'])
        self.top.geometry("340x120")
        self.top.transient(root)
        self.top.grab_set()
        tk.Label(self.top, text=L['find_replace'].split('...')[0] + ":").grid(row=0, column=0, sticky='e')
        self.entry_search = tk.Entry(self.top, width=25)
        self.entry_search.grid(row=0, column=1, padx=5, pady=4)
        tk.Button(self.top, text="Next / Suivant", command=self.trouver).grid(row=0, column=2, padx=5)
        tk.Label(self.top, text=L['find_replace'].split('/')[0] + " by / par:").grid(row=1, column=0, sticky='e')
        self.entry_replace = tk.Entry(self.top, width=25)
        self.entry_replace.grid(row=1, column=1, padx=5)
        tk.Button(self.top, text="Replace", command=self.remplacer).grid(row=1, column=2, padx=5)
        tk.Button(self.top, text="Replace All", command=self.remplacer_tout).grid(row=2, column=1, pady=7)
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
            messagebox.showinfo("Search / Recherche", "No more matches / Plus d'occurrence.")
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
        messagebox.showinfo("Replace All", f"{n} replaced.")

class BlocNotesOnglets:
    def __init__(self, root):
        self.root = root
        self.lang = 'en'
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        self.onglets = []
        self.recents = []
        self.max_recents = 10
        self.build_menus()
        self.ajouter_onglet()

    def build_menus(self):
        menubar = tk.Menu(self.root)
        L = LANG[self.lang]
        # File
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label=L['new_tab'], command=self.ajouter_onglet)
        filemenu.add_command(label=L['open'], command=lambda: self.onglet_courant().ouvrir())
        filemenu.add_command(label=L['save'], command=lambda: self.onglet_courant().enregistrer())
        filemenu.add_command(label=L['saveas'], command=lambda: self.onglet_courant().enregistrer_sous())
        filemenu.add_separator()
        filemenu.add_command(label=L['close_tab'], command=self.fermer_onglet)
        filemenu.add_command(label=L['quit'], command=self.demande_fermeture)
        menubar.add_cascade(label=L['file'], menu=filemenu)
        # Recent files
        self.recent_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=L['recent'], menu=self.recent_menu)
        self.maj_menu_recents()
        # Edit
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label=L['undo'], command=lambda: self.onglet_courant().text.event_generate('<<Undo>>'))
        editmenu.add_separator()
        editmenu.add_command(label=L['cut'], command=lambda: self.onglet_courant().text.event_generate('<<Cut>>'))
        editmenu.add_command(label=L['copy'], command=lambda: self.onglet_courant().text.event_generate('<<Copy>>'))
        editmenu.add_command(label=L['paste'], command=lambda: self.onglet_courant().text.event_generate('<<Paste>>'))
        editmenu.add_separator()
        editmenu.add_command(label=L['select_all'], command=lambda: self.onglet_courant().selectionner_tout())
        menubar.add_cascade(label=L['edit'], menu=editmenu)
        # Tools
        searchmenu = tk.Menu(menubar, tearoff=0)
        searchmenu.add_command(label=L['find_replace'], command=lambda: self.onglet_courant().ouvrir_rechercher())
        searchmenu.add_command(label=L['auto_save_on'], command=lambda: self.onglet_courant().demarrer_auto_save())
        searchmenu.add_command(label=L['auto_save_off'], command=lambda: self.onglet_courant().stopper_auto_save())
        searchmenu.add_command(label=L['global_search'], command=self.rechercher_tous_onglets)
        searchmenu.add_command(label=L['readonly_on'], command=lambda: self.onglet_courant().set_lecture_seule(True))
        searchmenu.add_command(label=L['readonly_off'], command=lambda: self.onglet_courant().set_lecture_seule(False))
        # Extra tools
        searchmenu.add_command(label=L['word_wrap'], command=lambda: self.onglet_courant().toggle_word_wrap())
        searchmenu.add_command(label=L['lock_tab'], command=lambda: self.onglet_courant().lock_tab(True))
        searchmenu.add_command(label=L['unlock_tab'], command=lambda: self.onglet_courant().lock_tab(False))
        searchmenu.add_command(label=L['goto_line'], command=lambda: self.onglet_courant().go_to_line())
        searchmenu.add_command(label=L['upper'], command=lambda: self.onglet_courant().to_upper())
        searchmenu.add_command(label=L['lower'], command=lambda: self.onglet_courant().to_lower())
        searchmenu.add_command(label=L['duplicate_line'], command=lambda: self.onglet_courant().duplicate_line())
        searchmenu.add_command(label=L['show_invisibles'], command=lambda: self.onglet_courant().show_invisibles())
        searchmenu.add_command(label=L['insert_timestamp'], command=lambda: self.onglet_courant().insert_timestamp())
        # Snippets sous-menu
        snipmenu = tk.Menu(searchmenu, tearoff=0)
        snipmenu.add_command(label=L['snippet_header'], command=lambda: self.onglet_courant().inserer_snippet(L['snippet_header']))
        snipmenu.add_command(label=L['snippet_signature'], command=lambda: self.onglet_courant().inserer_snippet(L['snippet_signature']))
        snipmenu.add_command(label=L['snippet_date'], command=lambda: self.onglet_courant().inserer_snippet(L['snippet_date']))
        searchmenu.add_cascade(label=L['snippets'], menu=snipmenu)
        searchmenu.add_command(label=L['color_html'], command=lambda: self.onglet_courant().coloration_html_css())
        menubar.add_cascade(label=L['tools'], menu=searchmenu)
        # View
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label=L['font'], command=lambda: self.onglet_courant().changer_police())
        viewmenu.add_command(label=L['fontsize'], command=lambda: self.onglet_courant().changer_taille())
        viewmenu.add_separator()
        viewmenu.add_command(label=L['theme'], command=lambda: self.onglet_courant().toggle_theme())
        menubar.add_cascade(label=L['view'], menu=viewmenu)
        # Language
        langmenu = tk.Menu(menubar, tearoff=0)
        langmenu.add_command(label="English", command=lambda: self.set_language('en'))
        langmenu.add_command(label="Français", command=lambda: self.set_language('fr'))
        menubar.add_cascade(label=L['language'], menu=langmenu)
        self.root.config(menu=menubar)
        # Shortcuts
        self.root.bind('<Control-s>', lambda e: self.onglet_courant().enregistrer())
        self.root.bind('<Control-S>', lambda e: self.onglet_courant().enregistrer())
        self.root.bind('<Control-o>', lambda e: self.onglet_courant().ouvrir())
        self.root.bind('<Control-O>', lambda e: self.onglet_courant().ouvrir())
        self.root.bind('<Control-q>', lambda e: self.demande_fermeture())
        self.root.bind('<Control-Q>', lambda e: self.demande_fermeture())
        self.root.bind('<Control-a>', lambda e: self.onglet_courant().selectionner_tout())
        self.root.bind('<Control-A>', lambda e: self.onglet_courant().selectionner_tout())
        self.root.bind('<Control-f>', lambda e: self.onglet_courant().ouvrir_rechercher())
        self.root.bind('<Control-F>', lambda e: self.onglet_courant().ouvrir_rechercher())
        self.root.protocol("WM_DELETE_WINDOW", self.demande_fermeture)

    def set_language(self, lang):
        self.lang = lang
        self.build_menus()
        for idx, ong in enumerate(self.onglets):
            title = os.path.basename(ong.file_path) if ong.file_path else LANG[self.lang]['tab_new']
            if ong.locked:
                title += " " + LANG[self.lang]['tab_locked']
            self.notebook.tab(idx, text=title)
            ong.maj_statut()

    def ajouter_onglet(self):
        frame = tk.Frame(self.notebook)
        def maj_nom_onglet(nom):
            self.notebook.tab(frame, text=nom)
        editeur = MiniBlocNotes(frame, lambda: self.lang, on_tab_title_change=maj_nom_onglet)
        self.notebook.add(frame, text=LANG[self.lang]['tab_new'])
        self.onglets.append(editeur)
        self.notebook.select(len(self.onglets)-1)
        return editeur

    def fermer_onglet(self):
        L = LANG[self.lang]
        idx = self.notebook.index(self.notebook.select())
        if self.onglets[idx].locked:
            messagebox.showwarning("Tab Lock", L['tab_locked_msg'])
            return
        if len(self.onglets) <= 1:
            messagebox.showinfo(L['file'], L['cannot_close_last_tab'])
            return
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

    # -------- Recent files
    def add_to_recents(self, path):
        if path and path not in self.recents:
            self.recents.insert(0, path)
            self.recents = self.recents[:self.max_recents]
        self.maj_menu_recents()
    def maj_menu_recents(self):
        self.recent_menu.delete(0, tk.END)
        for path in self.recents:
            self.recent_menu.add_command(label=path, command=lambda p=path: self.open_recent_file(p))
    def open_recent_file(self, path):
        ong = self.ajouter_onglet()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            ong.text.delete(1.0, tk.END)
            ong.text.insert(tk.END, contenu)
            ong.file_path = path
        except:
            messagebox.showerror("Error", f"Cannot open {path}")

    # -------- Search in all tabs
    def rechercher_tous_onglets(self):
        L = LANG[self.lang]
        terme = simpledialog.askstring(L['global_search'], L['find_replace'].split('...')[0] + " :")
        if not terme:
            return
        resultats = []
        for idx, ong in enumerate(self.onglets):
            contenu = ong.text.get(1.0, tk.END)
            lignes = contenu.splitlines()
            for num, ligne in enumerate(lignes, 1):
                if terme in ligne:
                    title = os.path.basename(ong.file_path) if ong.file_path else L['tab_new']
                    resultats.append(f"{title} (Tab {idx+1}), line {num}: {ligne.strip()}")
        if resultats:
            messagebox.showinfo(L['results'], "\n".join(resultats[:20]) + (f"\n...({len(resultats)-20} more)" if len(resultats) > 20 else ""))
        else:
            messagebox.showinfo(L['results'], L['none_found'])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("NoteSharp") 
    root.geometry("800x600")    
    app = BlocNotesOnglets(root)
    root.mainloop()
