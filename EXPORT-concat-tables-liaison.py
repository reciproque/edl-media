import os
import pandas as pd

input_dir = "tables"
output_csv = "LIAISON.csv"

colonnes_a_garder = [
    "Catégorie",
    "Type",
    "Nombre"
]

csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".csv")]

dataframes = []

for file in csv_files:
    filepath = os.path.join(input_dir, file)
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin-1")
    
    df = df[[col for col in colonnes_a_garder if col in df.columns]]
    
    dataframes.append(df)

result = pd.concat(dataframes, ignore_index=True)

result = result.reindex(columns=colonnes_a_garder)

result.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ {len(csv_files)} fichiers concaténés → {output_csv}")
