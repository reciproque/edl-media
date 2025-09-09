import pandas as pd
from rapidfuzz import process, fuzz
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

df1 = pd.read_csv("corpus-clean.csv", sep=";")
df2 = pd.read_csv("rmn-clean.csv", sep=";")

# Normalisation
for col in ['nom', 'auteur', 'lieu']:
    df1[col + '_norm'] = df1[col].apply(normalize_text)
    df2[col + '_norm'] = df2[col].apply(normalize_text)

# Préparer les colonnes
cols_df1 = df1.columns.drop([c for c in df1.columns if c.endswith('_norm')]).tolist()
cols_df2 = df2.columns.drop([c for c in df2.columns if c.endswith('_norm')]).tolist()
cols_df2_renamed = [c + "_df2" for c in cols_df2]

# Dictionnaires pour matching rapide
nom_choices = df2['nom_norm'].tolist()
auteur_choices = df2['auteur_norm'].tolist()
lieu_choices = df2['lieu_norm'].tolist()

with open("correspondances-opti.csv", "w", encoding="utf-8") as f_out:
    header = cols_df1 + cols_df2_renamed + ["score_nom", "score_auteur", "score_lieu"]
    f_out.write(",".join(header) + "\n")

    for _, row1 in tqdm(df1.iterrows(), total=len(df1), desc="Matching en cours"):

        # Trouver les meilleures correspondances individuelles
        best_nom = process.extractOne(row1['nom_norm'], nom_choices, scorer=fuzz.token_set_ratio)
        best_auteur = process.extractOne(row1['auteur_norm'], auteur_choices, scorer=fuzz.token_set_ratio)
        best_lieu = process.extractOne(row1['lieu_norm'], lieu_choices, scorer=fuzz.token_set_ratio)

        # Vérifier si les 3 correspondances pointent vers le même index
        indices = [nom_choices.index(best_nom[0]), auteur_choices.index(best_auteur[0]), lieu_choices.index(best_lieu[0])]
        idx_counter = pd.Series(indices).value_counts()

        best_idx2 = idx_counter.idxmax()  # l'index qui revient le plus

        # Récupérer les lignes
        row2 = df2.iloc[best_idx2]

        # Valeurs à écrire
        vals_df1 = [row1[c] for c in cols_df1]
        vals_df2 = [row2[c] for c in cols_df2]

        def escape_csv(val):
            if pd.isna(val):
                return ""
            s = str(val)
            if ',' in s or '"' in s:
                s = s.replace('"', '""')
                return f'"{s}"'
            return s

        vals_df1_escaped = [escape_csv(v) for v in vals_df1]
        vals_df2_escaped = [escape_csv(v) for v in vals_df2]

        line = ",".join(vals_df1_escaped + vals_df2_escaped +
                        [f"{best_nom[1]:.1f}", f"{best_auteur[1]:.1f}", f"{best_lieu[1]:.1f}"]) + "\n"
        f_out.write(line)

print("\n✅ Matching terminé.")
