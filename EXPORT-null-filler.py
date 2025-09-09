import pandas as pd

input_csv = "_MASTER-_EXPORT 28.08.25.csv"
output_csv = "MASTER"

# Lire le CSV
df = pd.read_csv(input_csv, dtype=str)  # dtype=str pour garder tout en texte

# Remplacer les valeurs manquantes ou vides par 'null'
df = df.fillna("null")  # NaN → 'null'
df = df.replace(r'^\s*$', 'null', regex=True)  # cellules vides ou avec juste des espaces → 'null'

# Sauvegarder
df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ Fichier transformé → {output_csv}")
