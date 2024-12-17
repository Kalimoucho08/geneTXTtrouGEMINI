import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import spacy
import random
import google.generativeai as genai
import os

# Configurez votre clé API
genai.configure(api_key="")

# Charger le modèle français de spaCy
nlp = spacy.load("fr_core_news_sm")

class TexteApp:
    def __init__(self, master):
        self.master = master
        master.title("Générateur de Texte et Texte à Trous")
        master.geometry("950x750")
        
        #Initialisation des variables.
        self.show_list_var = tk.BooleanVar(value=False)
        self.original_text_var = tk.StringVar(value="Ne pas inclure")
        self.distribute_holes_var = tk.BooleanVar(value=False)
        self.api_key = self.load_api_key() # Charge l'API key au démarrage
        
        # --- Panneau pour la source du texte ---
        self.source_frame = ttk.LabelFrame(master, text="Source du Texte")
        self.source_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Boutons pour la source du texte
        button_source_frame = ttk.Frame(self.source_frame)
        button_source_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        
        self.paste_button = ttk.Button(button_source_frame, text="Coller", command=self.paste_text, width=8)
        self.paste_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.open_button = ttk.Button(button_source_frame, text="Ouvrir", command=self.open_file, width=8)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.gemini_button = ttk.Button(button_source_frame, text="Gemini", command=self.open_gemini_window, width=8, state = tk.NORMAL if self.api_key else tk.DISABLED)
        self.gemini_button.pack(side=tk.LEFT, padx=5, pady=5)
        
         # API Key Input
        self.api_frame = ttk.Frame(self.source_frame)
        self.api_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        
        self.api_key_label = ttk.Label(self.api_frame, text="API Key :")
        self.api_key_label.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.api_key_entry = ttk.Entry(self.api_frame, width=30, show="*")
        self.api_key_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.api_save_button = ttk.Button(self.api_frame, text="Sauvegarder", command=self.save_api_key, width = 12)
        self.api_save_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Zone de texte pour le texte source
        self.text_label = ttk.Label(self.source_frame, text="Texte Source:")
        self.text_label.pack(pady=5)
        self.text_entry = scrolledtext.ScrolledText(self.source_frame, height=10)
        self.text_entry.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # --- Panneau pour les options du texte à trous ---
        self.trous_frame = ttk.LabelFrame(master, text="Options du Texte à Trous")
        self.trous_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Nombre de mots à supprimer
        self.num_words_frame = ttk.Frame(self.trous_frame)
        self.num_words_frame.pack(pady=5, fill=tk.X)
        
        self.num_words_label = ttk.Label(self.num_words_frame, text="Nombre de mots :")
        self.num_words_label.pack(side=tk.LEFT, padx=5)
        self.num_words_entry = ttk.Entry(self.num_words_frame, width=10)
        self.num_words_entry.pack(side=tk.LEFT, padx=5)

        # Types de mots à supprimer (en deux colonnes)
        self.types_frame = ttk.LabelFrame(self.trous_frame, text="Types de mots")
        self.types_frame.pack(pady=10, fill = tk.X, padx = 10)

        self.type_vars = {
            'Noms': tk.BooleanVar(),
            'Verbes': tk.BooleanVar(),
            'Adjectifs': tk.BooleanVar(),
            'Pronoms Personnels': tk.BooleanVar(),
            'Articles/Déterminants': tk.BooleanVar(),
            'Prépositions': tk.BooleanVar()
        }

        row, col = 0, 0
        for word_type, var in self.type_vars.items():
            cb = ttk.Checkbutton(self.types_frame, text=word_type, variable=var)
            cb.grid(row=row, column=col, padx=5, pady=2, sticky='w')
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Options d'affichage
        self.option_frame = ttk.Frame(self.trous_frame)
        self.option_frame.pack(pady=5, fill=tk.X)

        self.show_list_check = ttk.Checkbutton(self.option_frame, text="Liste des mots", variable=self.show_list_var)
        self.show_list_check.pack(side=tk.LEFT, padx=5,pady = 5)

        self.original_text_label = ttk.Label(self.option_frame, text="Texte original :")
        self.original_text_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.original_text_menu = ttk.Combobox(self.option_frame, textvariable=self.original_text_var, width=15)
        self.original_text_menu['values'] = ["Ne pas inclure", "Avant", "Après"]
        self.original_text_menu.pack(side=tk.LEFT, padx=5, pady=5)

        self.distribute_holes_check = ttk.Checkbutton(self.option_frame, text="Répartir les trous", variable=self.distribute_holes_var)
        self.distribute_holes_check.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame pour les boutons générer/sauvegarder
        self.button_frame = ttk.Frame(self.trous_frame)
        self.button_frame.pack(pady=10, fill=tk.X)

        self.generate_button = ttk.Button(self.button_frame, text="Générer",
                                            command=self.generate_texte_a_trous, width=12)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        self.save_odt_button = ttk.Button(self.button_frame, text="Sauvegarder Texte", command=self.save_to_text, width=12)
        self.save_odt_button.pack(side=tk.LEFT, padx=5)
      
        # Variables
        self.gemini_window = None
        self.result_window = None
        self.result_text = None

    def paste_text(self):
        try:
            text = self.master.clipboard_get()
            self.text_entry.insert(tk.END, text)
        except tk.TclError:
            messagebox.showerror("Erreur", "Le presse-papier est vide.")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers Texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.text_entry.delete("1.0", tk.END)
                    self.text_entry.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def open_gemini_window(self):
        if not self.gemini_window or not tk.Toplevel.winfo_exists(self.gemini_window):
            self.gemini_window = tk.Toplevel(self.master)
            self.gemini_window.title("Générateur de texte scolaire avec Gemini")

            # Zone pour écrire le prompt général
            general_prompt_label = tk.Label(self.gemini_window, text="Écrivez votre prompt général :")
            general_prompt_label.pack()

            general_prompt_entry = scrolledtext.ScrolledText(self.gemini_window, wrap=tk.WORD, width=50, height=5)
            general_prompt_entry.pack()

            # Zone pour sélectionner le niveau de classe
            niveau_label = tk.Label(self.gemini_window, text="Sélectionnez le niveau de classe :")
            niveau_label.pack()
            niveau_combobox = ttk.Combobox(self.gemini_window, values=["CP", "CE1", "CE2", "CM1", "CM2"])
            niveau_combobox.pack()

            # Zone pour sélectionner le type littéraire
            type_label = tk.Label(self.gemini_window, text="Sélectionnez le type littéraire :")
            type_label.pack()
            type_combobox = ttk.Combobox(self.gemini_window, values=["conte", "poème", "narration", "description"])
            type_combobox.pack()

            # Zone pour entrer le nombre minimum et maximum de phrases
            phrases_label = tk.Label(self.gemini_window, text="Nombre minimum et maximum de phrases :")
            phrases_label.pack()

            min_phrases_entry = tk.Entry(self.gemini_window)
            min_phrases_entry.insert(0, "Min")
            min_phrases_entry.pack()

            max_phrases_entry = tk.Entry(self.gemini_window)
            max_phrases_entry.insert(0, "Max")
            max_phrases_entry.pack()

            # Bouton pour générer le texte
            generate_button = tk.Button(self.gemini_window, text="Générer",
                                        command=lambda: self.on_gemini_generate(
                                            general_prompt_entry.get("1.0", tk.END).strip(),
                                            niveau_combobox.get(),
                                            type_combobox.get(),
                                            min_phrases_entry.get(),
                                            max_phrases_entry.get()
                                        ))
            generate_button.pack()
            
    def on_gemini_generate(self, general_prompt, niveau_classe, type_litteraire, min_phrases, max_phrases):
        if not self.api_key:
            messagebox.showerror("Erreur", "Veuillez entrer une API key pour utiliser cette fonctionnalité")
            return
        
        genai.configure(api_key=self.api_key)
        prompt = f"{general_prompt} Écris un texte de type '{type_litteraire}' pour un élève de {niveau_classe}. "
        
        if min_phrases and max_phrases:
             prompt += f"Le texte doit contenir entre {min_phrases} et {max_phrases} phrases."

        generated_output = self.generate_text(prompt)
        self.text_entry.delete("1.0", tk.END)
        self.text_entry.insert(tk.END, generated_output)
        self.gemini_window.destroy() #fermeture de la fenetre
        self.gemini_window = None
        
    def generate_text(self, prompt):
         model = genai.GenerativeModel("gemini-1.5-flash")
         response = model.generate_content(prompt)
         return response.text
    
    def open_result_window(self, text_to_show):
         if not self.result_window or not tk.Toplevel.winfo_exists(self.result_window):
            self.result_window = tk.Toplevel(self.master)
            self.result_window.title("Texte à Trous Généré")
            
            self.result_text = scrolledtext.ScrolledText(self.result_window, height=15, wrap=tk.WORD)
            self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            #Ajout du bouton de copie
            copy_button = ttk.Button(self.result_window, text="Copier le texte", command=self.copy_text)
            copy_button.pack(side=tk.TOP, padx=10, pady=5, anchor='w')
            
            self.result_text.insert(tk.END, text_to_show)
            self.result_text.config(state=tk.DISABLED)

         else:
            self.result_window.focus()
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            
            #Ajout du bouton de copie
            copy_button = ttk.Button(self.result_window, text="Copier le texte", command=self.copy_text)
            copy_button.pack(side=tk.TOP, padx=10, pady=5, anchor='w')
            
            self.result_text.insert(tk.END, text_to_show)
            self.result_text.config(state=tk.DISABLED)
    
    def generate_texte_a_trous(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        original_text = text # sauvegarde du texte original

        if not text:
            messagebox.showerror("Erreur", "Veuillez entrer un texte.")
            return

        try:
            num_words = int(self.num_words_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide de mots à supprimer.")
            return

        selected_types = [t for t, var in self.type_vars.items() if var.get()]

        if not selected_types:
            messagebox.showerror("Erreur", "Veuillez sélectionner au moins un type de mot à supprimer.")
            return

        doc = nlp(text)

        type_mapping = {
            'Noms': ['NOUN', 'PROPN'],
            'Verbes': ['VERB', 'AUX'],
            'Adjectifs': ['ADJ'],
            'Pronoms Personnels': ['PRON'],
            'Articles/Déterminants': ['DET'],
            'Prépositions': ['ADP']
        }

        eligible_tokens = [token for token in doc if any(token.pos_ == pos for type in selected_types for pos in type_mapping[type])]

        if num_words > len(eligible_tokens):
            num_words = len(eligible_tokens)
        
        removed_words = []
        # Répartition des trous de manière équilibrée
        if self.distribute_holes_var.get():
            sentences = list(doc.sents)
            num_sentences = len(sentences)
            if num_sentences > 0 :
               holes_per_sentence = num_words // num_sentences
               remaining_holes = num_words % num_sentences
            else :
                holes_per_sentence = 0
                remaining_holes = 0
               
            tokens_to_remove = []
            current_token = 0
            for i, sentence in enumerate(sentences):
                
                sentence_eligible_tokens = [token for token in sentence if any(token.pos_ == pos for type in selected_types for pos in type_mapping[type])]

                if not sentence_eligible_tokens :
                  continue
                
                num_holes = holes_per_sentence
                if i < remaining_holes:
                  num_holes += 1
                
                if num_holes > len(sentence_eligible_tokens):
                     num_holes = len(sentence_eligible_tokens)
                     
                if num_holes > 0 :
                 sampled_tokens = random.sample(sentence_eligible_tokens, num_holes)
                 tokens_to_remove.extend(sampled_tokens)
                 removed_words.extend([token.text for token in sampled_tokens])
                
        else :
           tokens_to_remove = random.sample(eligible_tokens, num_words)
           removed_words = [token.text for token in tokens_to_remove]


        result_words = []
        
        # Remplacement des mots par des trous proportionnels sans césure
        for token in doc:
            if token in tokens_to_remove:
                gap_length = max(1, len(token.text) // 2 + 1)
                gap = '__' * gap_length
                result_words.append(gap)
            else:
                result_words.append(token.text)
        
        result_text = " ".join(result_words)
        
        # Gestion de la liste des mots supprimés
        list_text = ""
        if self.show_list_var.get():
            list_text = ", ".join(sorted(removed_words))
        
        # Ajout du texte original, du texte à trous et de la liste des mots
        text_to_show = ""
        if self.original_text_var.get() == "Avant":
             text_to_show = f"Texte original:\n\n{original_text}\n\n\nTexte à trous:\n\n{result_text}"
        elif self.original_text_var.get() == "Après" :
             text_to_show = f"Texte à trous:\n\n{result_text}\n\n\nTexte original:\n\n{original_text}"
        else :
            text_to_show = f"Texte à trous:\n\n{result_text}"

        if list_text:
            text_to_show += f"\n\n\nListe des mots supprimés : {list_text}"
        
        self.open_result_window(text_to_show)
    
    def copy_text(self):
        if self.result_text :
           text_to_copy = self.result_text.get("1.0", tk.END)
           self.master.clipboard_clear()
           self.master.clipboard_append(text_to_copy)
        else :
            messagebox.showerror("Erreur", "Aucun texte généré.")
    
    def save_to_text(self, file_path = None):
         if not self.result_window or not tk.Toplevel.winfo_exists(self.result_window):
            messagebox.showerror("Erreur", "Aucun texte à trous n'a été généré.")
            return
         
         text_to_save = self.result_text.get("1.0",tk.END).strip()
         
         if not text_to_save :
            messagebox.showerror("Erreur", "Aucun texte à trous n'a été généré.")
            return
        
         if file_path == None :
           file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Fichier texte", "*.txt"),
                                                            ("Tous les fichiers", "*.*")])
         
         if file_path:
             try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_to_save)
                messagebox.showinfo("Succès", f"Le fichier a été sauvegardé avec succès à l'emplacement :\n{file_path}")
             except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue lors de la sauvegarde :\n{str(e)}")
                
    def save_api_key(self):
        api_key = self.api_key_entry.get().strip()
        self.api_key = api_key
        if api_key:
            try:
                with open("api_key.txt", "w") as f:
                    f.write(api_key)
                messagebox.showinfo("Succès", "API key sauvegardée.")
                self.gemini_button.config(state = tk.NORMAL)
            except Exception as e :
                 messagebox.showerror("Erreur", f"Une erreur est survenue lors de la sauvegarde de l'api key:\n{str(e)}")
        else :
             messagebox.showerror("Erreur", "L'api key ne doit pas être vide.")
             
    def load_api_key(self):
        try:
            if os.path.exists("api_key.txt"):
              with open("api_key.txt", "r") as f:
                return f.read().strip()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors du chargement de l'api key:\n{str(e)}")
            return None

# Exécution de l'application
root = tk.Tk()
app = TexteApp(root)
root.mainloop()
