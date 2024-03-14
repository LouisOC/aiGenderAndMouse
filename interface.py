import threading
import tkinter as tk
from functools import partial
from tkinter import ttk

from aiMouse import aiMouse
from gender_age import start_detection  # Importez la fonction depuis gender_age.py

choice2_count = 0

def start_gender_age_detection():
    def run_detection():
        global choice2_count  # Utilisation de la variable globale

        def on_choice_selected(choice):
            global choice2_count  # Utilisation de la variable globale
            choices_window.destroy()  # Ferme la fenêtre de choix
            if choice == 1:
                start_detection()
            elif choice == 2:
                choice2_count += 1
                if choice2_count == 2:
                    error_window = tk.Toplevel(root)
                    error_window.title("Erreur")
                    error_window.geometry("400x100")
                    error_window.minsize(300, 100)

                    label = tk.Label(error_window, text="Erreur : Tu ne mérites pas d'essayer l'application en fait...", fg="red")
                    label.pack(pady=20)

                    root.after(3000, root.destroy)             # Ferme l'application
                else:
                    error_window = tk.Toplevel(root)
                    error_window.title("Erreur")
                    error_window.geometry("300x100")
                    error_window.minsize(300, 100)

                    label = tk.Label(error_window, text="Erreur : Ca n'existe pas, tu t'es fais avoir", fg="red")
                    label.pack(pady=20)

        choices_window = tk.Toplevel(root)
        choices_window.title("Choix")
        choices_window.geometry("300x200")
        choices_window.minsize(300, 200)

        label = tk.Label(choices_window, text="Choisissez une option:")
        label.pack(pady=10)
        # Fonction à appeler lorsque l'utilisateur sélectionne une option
        btn_choice1 = ttk.Button(choices_window, text="Homme/Femme", command=partial(on_choice_selected, 1))
        btn_choice1.pack(pady=5)

        btn_choice2 = ttk.Button(choices_window, text="Autres/Identification objet",
                                 command=partial(on_choice_selected, 2))
        btn_choice2.pack(pady=5)

    # Planifiez l'exécution de la détection dans le thread principal
    root.after(0, run_detection)

def start_ai_mouse():
    print("Démarrage de la souris IA...")  # Code de la fonction start_ai_mouse reste inchangé
    def run_detection():
        aiMouse()  # Appelez la fonction importée de gender_age.py

        # Planifiez l'exécution de la détection dans le thread principal

    root.after(0, run_detection)

root = tk.Tk()
root.title("Sélecteur de Programme IA")
root.geometry("400x200")
root.minsize(400, 200)

style = ttk.Style(root)
style.theme_use('clam')
style.configure('TButton', font=('Helvetica', 12), borderwidth='4')
style.map('TButton', foreground=[('active', '!disabled', 'green')], background=[('active', 'black')])

def run_threaded_job(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

gender_age_btn = ttk.Button(root, text="Détection Genre/Age", command=lambda: run_threaded_job(start_gender_age_detection))
gender_age_btn.pack(expand=True)

ai_mouse_btn = ttk.Button(root, text="Souris IA", command=lambda: run_threaded_job(start_ai_mouse))
ai_mouse_btn.pack(expand=True)

root.mainloop()
