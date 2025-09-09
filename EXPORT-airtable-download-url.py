import csv
import requests
import os

input_csv = "url-and-names.csv"

with open(input_csv, newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        query = (row.get('Image - pour validation - URL', '')).strip()
        if not query:
            continue

        filename = (row.get("Image - Nom fichier", '')).strip()
        if not filename:
            continue

        # Lire la colonne Année
        annee = (row.get("Année", "")).strip()

        # Créer un dossier par année (HGA1, HGA2, HGA3, etc.)
        if annee not in ("HGA1", "HGA2", "HGA3"):
            print(f"⚠️ Année inconnue '{annee}' pour {filename}, ignoré")
            continue

        output_dir = os.path.join(".", annee)
        os.makedirs(output_dir, exist_ok=True)

        # Faire une requête
        response = requests.get(query, stream=True)
        if response.status_code == 200:
            # Récupérer le Content-Type
            content_type = response.headers.get("Content-Type", "").lower()

            # Déduire l'extension
            ext = ""
            if "jpeg" in content_type:
                ext = ".jpg"
            elif "png" in content_type:
                ext = ".png"
            elif "gif" in content_type:
                ext = ".gif"
            elif "webp" in content_type:
                ext = ".webp"
            elif "bmp" in content_type:
                ext = ".bmp"
            elif "tiff" in content_type:
                ext = ".tif"

            # Ajouter l'extension si manquante
            if not filename.lower().endswith(ext):
                filename += ext

            # Chemin complet de sortie
            filepath = os.path.join(output_dir, filename)

            # Sauvegarder le fichier
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"✅ {query} → {filepath} ({content_type})")
        else:
            print(f"❌ Erreur {response.status_code} pour {query}")
