import pandas as pd
from rapidfuzz import fuzz
import unidecode
import re

def normalize_text(s):
    if pd.isna(s):
        return ""
    s = s.lower()
    s = unidecode.unidecode(s)  # enlève accents
    s = re.sub(r"[^\w\s]", "", s)  # enlève ponctuation
    s = re.sub(r"\s+", " ", s).strip()  # espaces multiples → 1 espace
    return s

df1 = pd.read_csv("corpus-clean.csv", sep=";")
df2 = pd.read_csv("rmn-clean.csv", sep=";")

# Normalisation des colonnes dans les deux dfs
for col in ['nom', 'auteur', 'lieu']:
    df1[col + '_norm'] = df1[col].apply(normalize_text)
    df2[col + '_norm'] = df2[col].apply(normalize_text)

total = len(df1)
bar_length = 40

with open("correspondances-better.csv", "w", encoding="utf-8") as f_out:
    cols_df1 = df1.columns.drop([c for c in df1.columns if c.endswith('_norm')]).tolist()
    cols_df2 = df2.columns.drop([c for c in df2.columns if c.endswith('_norm')]).tolist()
    cols_df2_renamed = [c + "_df2" for c in cols_df2]

    header = cols_df1 + cols_df2_renamed + ["similarity_score"]
    f_out.write(",".join(header) + "\n")

    for i, (idx1, row1) in enumerate(df1.iterrows()):

        best_score = 0
        best_idx2 = None

        for idx2, row2 in df2.iterrows():
            score_nom = fuzz.token_set_ratio(row1['nom_norm'], row2['nom_norm'])
            score_auteur = fuzz.token_set_ratio(row1['auteur_norm'], row2['auteur_norm'])
            score_lieu = fuzz.token_set_ratio(row1['lieu_norm'], row2['lieu_norm'])

            combined_score = 0.5 * score_nom + 0.3 * score_auteur + 0.2 * score_lieu

            if combined_score > best_score:
                best_score = combined_score
                best_idx2 = idx2

        row2 = df2.loc[best_idx2]

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

        line = ",".join(vals_df1_escaped + vals_df2_escaped + [f"{best_score:.1f}"]) + "\n"
        f_out.write(line)

        progress = (i + 1) / total
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\rMatching en cours |{bar}| {int(progress * 100)}%', end='')

print('\n✅ Matching terminé.')
