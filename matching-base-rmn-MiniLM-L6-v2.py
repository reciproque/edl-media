import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Charger les bases
df1 = pd.read_csv("base1.csv")
df2 = pd.read_csv("base2.csv")

# Nettoyage simple
def clean(text):
    return str(text).strip().lower()

df1['nom_clean'] = df1['nom'].apply(clean)
df2['nom_clean'] = df2['nom'].apply(clean)

# Charger le modèle Sentence-BERT
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Encoder les noms
embeddings1 = model.encode(df1['nom_clean'].tolist(), convert_to_tensor=True)
embeddings2 = model.encode(df2['nom_clean'].tolist(), convert_to_tensor=True)

# Calcul de la similarité cosinus
cosine_scores = util.cos_sim(embeddings1, embeddings2)

# Récupérer les meilleures correspondances avec toutes les colonnes de df2
matched_rows = []
for i, row in enumerate(cosine_scores):
    best_idx = row.argmax().item()
    best_score = row[best_idx].item()
    
    if best_score > 0.80:
        matched_data = df2.iloc[best_idx].to_dict()
    else:
        matched_data = {col: "" for col in df2.columns}
    
    matched_data["similarité"] = round(best_score, 4)
    matched_rows.append(matched_data)

# Fusionner les données dans df1
df_matched = pd.DataFrame(matched_rows)
df_final = pd.concat([df1, df_matched], axis=1)

# Export
df_final.to_csv("base1_avec_infos_base2.csv", index=False)

print("✅ Fichier enrichi avec toutes les colonnes exporté sous 'base1_avec_infos_base2.csv'")
