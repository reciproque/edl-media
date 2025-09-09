import pandas as pd
import numpy as np
from rapidfuzz import fuzz
import unidecode
import re
from tqdm import tqdm

def normalize_text(s):
    if pd.isna(s):
        return ""
    s = s.lower()
    s = unidecode.unidecode(s)
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# Chargement
df1 = pd.read_csv("corpus-clean.csv", sep=";")
df2 = pd.read_csv("rmn-clean.csv", sep=";")

# Normalisation
for col in ['nom', 'auteur', 'lieu']:
    df1[col + '_norm'] = df1[col].apply(normalize_text)
    df2[col + '_norm'] = df2[col].apply(normalize_text)

# Colonnes à exporter
cols_df1 = [c for c in df1.columns if not c.endswith('_norm')]
cols_df2 = [c for c in df2.columns if not c.endswith('_norm')]
cols_df2_renamed = [c + "_df2" for c in cols_df2]

# Index pour aller plus vite
df2_norm = df2[['nom_norm', 'auteur_norm', 'lieu_norm']].copy()

# Résultats
with open("correspondances-line.csv", "w", encoding="utf-8") as f_out:
    header = cols_df1 + cols_df2_renamed + ["score_total"]
    f_out.write(",".join(header) + "\n")

    for _, row1 in tqdm(df1.iterrows(), total=len(df1), desc="Matching en cours"):

        # Calcul des scores pour CHAQUE ligne de df2
        scores = df2_norm.apply(lambda row2: {
            "score_nom": fuzz.token_set_ratio(row1['nom_norm'], row2['nom_norm']),
            "score_auteur": fuzz.token_set_ratio(row1['auteur_norm'], row2['auteur_norm']),
            "score_lieu": fuzz.token_set_ratio(row1['lieu_norm'], row2['lieu_norm']),
        }, axis=1)

        # Création DataFrame temporaire avec les scores
        score_df = pd.DataFrame(scores.tolist())
        score_df["total"] = 0.5 * score_df["score_nom"] + 0.3 * score_df["score_auteur"] + 0.2 * score_df["score_lieu"]

        best_idx = score_df["total"].idxmax()
        best_score = score_df.loc[best_idx, "total"]

        row2 = df2.loc[best_idx]

        # Préparer export
        def escape_csv(val):
            if pd.isna(val):
                return ""
            s = str(val)
            if ',' in s or '"' in s:
                s = s.replace('"', '""')
                return f'"{s}"'
            return s

        vals_df1 = [escape_csv(row1[c]) for c in cols_df1]
        vals_df2 = [escape_csv(row2[c]) for c in cols_df2]

        line = ",".join(vals_df1 + vals_df2 + [f"{best_score:.1f}"]) + "\n"
        f_out.write(line)

print("\n✅ Matching terminé.")
