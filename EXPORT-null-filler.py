import pandas as pd
import re

input_csv = "_MASTER-POUR EXPORT.csv"
output_csv = "MASTER.csv"

df = pd.read_csv(input_csv, dtype=str)

df = df.fillna("null") 
df = df.replace(r'^\s*$', 'null', regex=True)
colonnes_cibles = ["Matériaux", "Techniques", "Sphère culturelle", "Aire culturelle"]

for col in colonnes_cibles:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: re.sub(r',\s*', ', ', x) if isinstance(x, str) else x)

df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ Fichier transformé → {output_csv}")
