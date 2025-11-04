import pandas as pd

input_csv = "_MASTER-POUR EXPORT.csv"
output_csv = "MASTER.csv"

df = pd.read_csv(input_csv, dtype=str)

df = df.fillna("null") 
df = df.replace(r'^\s*$', 'null', regex=True)

df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ Fichier transformé → {output_csv}")
