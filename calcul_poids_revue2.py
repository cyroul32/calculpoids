import tkinter as tk
from tkinter import messagebox

# Liste pour stocker les entrées
rows = []

def calculer_poids_ligne(row):
    """Calcule le poids de la ligne et met à jour l'affichage."""
    try:
        largeur = float(row["largeur"].get() or 0)
        hauteur = float(row["hauteur"].get() or 0)
        pages = int(row["pages"].get() or 0)
        grammage = float(row["grammage"].get() or 0)
        
        # Calcul de l'épaisseur (convertie en mm)
        epaisseur = 0.9 * (pages / 2) * (grammage / 1000)
        row["epaisseur"].config(text=f"{epaisseur:.2f} mm")

        # Calcul du poids
        poids = (largeur * hauteur * (pages / 2) * grammage) / 1_000_000
        row["resultat"].config(text=f"{poids:.2f} g")

        calculer_poids_total()
    except ValueError:
        row["resultat"].config(text="Erreur")
        row["epaisseur"].config(text="Erreur")

def calculer_poids_total():
    """Calcule le poids total de toutes les lignes et ajoute une marge de sécurité."""
    total_poids = sum(
        float(row["resultat"].cget("text").replace(" g", "") or 0)
        for row in rows
    )
    total_poids_arrondi = round(total_poids)
    poids_avec_marge = round(total_poids * 1.01)

    label_total.config(text=f"Poids total : {total_poids_arrondi} g")
    label_total_securite.config(text=f"Poids avec 1% de sécurité : {poids_avec_marge} g")

def ajouter_ligne():
    """Ajoute une nouvelle ligne pour entrer des valeurs."""
    row_frame = tk.Frame(frame_content)
    row_frame.pack(fill="x", pady=2)

    entry_largeur = tk.Entry(row_frame, width=10)
    entry_largeur.grid(row=0, column=0, padx=5)
    entry_hauteur = tk.Entry(row_frame, width=10)
    entry_hauteur.grid(row=0, column=1, padx=5)
    entry_pages = tk.Entry(row_frame, width=10)
    entry_pages.grid(row=0, column=2, padx=5)
    entry_grammage = tk.Entry(row_frame, width=10)
    entry_grammage.grid(row=0, column=3, padx=5)

    label_epaisseur = tk.Label(row_frame, text="0.00 mm", width=12, anchor="e")
    label_epaisseur.grid(row=0, column=4, padx=5)

    label_resultat = tk.Label(row_frame, text="0.00 g", width=12, anchor="e")
    label_resultat.grid(row=0, column=5, padx=5)

    btn_supprimer = tk.Button(row_frame, text="X", command=lambda: supprimer_ligne(row_frame))
    btn_supprimer.grid(row=0, column=6, padx=5)

    row_data = {
        "largeur": entry_largeur,
        "hauteur": entry_hauteur,
        "pages": entry_pages,
        "grammage": entry_grammage,
        "epaisseur": label_epaisseur,
        "resultat": label_resultat
    }

    rows.append(row_data)

    # Associer l'event pour recalculer en temps réel
    for entry in (entry_largeur, entry_hauteur, entry_pages, entry_grammage):
        entry.bind("<KeyRelease>", lambda event, r=row_data: calculer_poids_ligne(r))

def supprimer_ligne(row_frame):
    """Supprime une ligne et met à jour le poids total."""
    for i, row in enumerate(frame_content.winfo_children()):
        if row == row_frame:
            rows.pop(i)
            row_frame.destroy()
            calculer_poids_total()
            break

# Fenêtre principale
root = tk.Tk()
root.title("Calculateur de Poids de Revue")
root.geometry("800x450")

# En-tête des colonnes alignées
header_frame = tk.Frame(root)
header_frame.pack(pady=10)

tk.Label(header_frame, text="Largeur (mm)", width=10, anchor="w").grid(row=0, column=0, padx=5)
tk.Label(header_frame, text="Hauteur (mm)", width=10, anchor="w").grid(row=0, column=1, padx=5)
tk.Label(header_frame, text="Pages", width=10, anchor="w").grid(row=0, column=2, padx=5)
tk.Label(header_frame, text="Grammage (g/m²)", width=10, anchor="w").grid(row=0, column=3, padx=5)
tk.Label(header_frame, text="Épaisseur (mm)", width=12, anchor="e").grid(row=0, column=4, padx=5)
tk.Label(header_frame, text="Poids (g)", width=12, anchor="e").grid(row=0, column=5, padx=5)

# Conteneur des lignes dynamiques
frame_content = tk.Frame(root)
frame_content.pack()

# Ajouter une première ligne par défaut
ajouter_ligne()

# Bouton pour ajouter une ligne
btn_ajouter = tk.Button(root, text="Ajouter une ligne", command=ajouter_ligne)
btn_ajouter.pack(pady=10)

# Affichage du poids total arrondi
label_total = tk.Label(root, text="Poids total : 0 g", font=("Arial", 12))
label_total.pack(pady=5)

# Affichage du poids total avec 1% de sécurité
label_total_securite = tk.Label(root, text="Poids avec 1% de sécurité : 0 g", font=("Arial", 12))
label_total_securite.pack(pady=5)

# Lancer l'application
root.mainloop()
