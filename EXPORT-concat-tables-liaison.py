import os
import pandas as pd

# Dossier contenant les CSV
input_dir = "tables"
output_csv = "LIAISON.csv"

# Colonnes à conserver
colonnes_a_garder = [
    "Catégorie",
    "Type",
    "Nombre",
    "Nombre (Lieu d'origine)",
    "Nombre (Lieu de conservation)"
]

# Récupérer tous les fichiers .csv du dossier
csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".csv")]

dataframes = []

for file in csv_files:
    filepath = os.path.join(input_dir, file)
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin-1")
    
    # Ne garder que les colonnes d'intérêt (celles présentes dans le fichier)
    df = df[[col for col in colonnes_a_garder if col in df.columns]]
    
    dataframes.append(df)

# Concaténer en alignant les colonnes
result = pd.concat(dataframes, ignore_index=True)

# S'assurer que l'ordre des colonnes est correct
result = result.reindex(columns=colonnes_a_garder)

# Sauvegarder le CSV final
result.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ {len(csv_files)} fichiers concaténés → {output_csv}")
