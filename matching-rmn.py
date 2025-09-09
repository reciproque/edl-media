import pandas as pd
from rapidfuzz import process, fuzz

# Chargement avec le bon séparateur
df1 = pd.read_csv("corpus-clean-rmn-29-07.csv", sep=";")
df2 = pd.read_csv("rmn-clean.csv", sep=";")

def make_combined(row):
    parts = []

    # Nom est pondéré (répété deux fois par exemple)
    nom = str(row['nom']).strip().lower()
    if nom:
        parts.extend([nom] * 2)

    # Auteur (s’il est non vide)
    auteur = str(row['auteur']).strip().lower()
    if auteur:
        parts.append(auteur)

    # Lieu (s’il est non vide)
    lieu = str(row['lieu']).strip().lower()
    if lieu:
        parts.append(lieu)

    return ' '.join(parts).strip()

# Appliquer à chaque ligne
df1['combined'] = df1.apply(make_combined, axis=1)
df2['combined'] = df2.apply(make_combined, axis=1)

df2_combined = df2['combined'].tolist()

total = len(df1)
bar_length = 40

with open("correspondances-rmn-traite-gs-29-07.csv", "w", encoding="utf-8") as f_out:
    cols_df1 = df1.columns.drop('combined').tolist()
    cols_df2 = df2.columns.drop('combined').tolist()
    cols_df2_renamed = [c + "_df2" for c in cols_df2]

    header = cols_df1 + cols_df2_renamed + ["similarity_score"]
    f_out.write(",".join(header) + "\n")

    for i, (idx1, row1) in enumerate(df1.iterrows()):
        query = row1['combined']
        best_match = process.extractOne(query, df2_combined, scorer=fuzz.token_sort_ratio)

        if best_match:
            _, score, idx2 = best_match
            row2 = df2.iloc[idx2]

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

            line = ",".join(vals_df1_escaped + vals_df2_escaped + [str(score)]) + "\n"
            f_out.write(line)

        progress = (i + 1) / total
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\rMatching en cours |{bar}| {int(progress * 100)}%', end='')

print('\n✅ Matching terminé.')
