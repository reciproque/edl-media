import csv
import requests
import urllib.request
import os

def fetch_commons_image_info(search_query, n, max_results=10):
    """Télécharge une image Wikimedia Commons et retourne (filename, url) ou ('','')"""
    try:
        search_url = "https://commons.wikimedia.org/w/api.php"
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search_query,
            "srnamespace": 6,
            "srlimit": max_results
        }

        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()
        search_results = search_data.get("query", {}).get("search", [])

        for result in search_results:
            file_title = result["title"]  # ex: "File:Mona Lisa.jpg"

            imageinfo_params = {
                "action": "query",
                "format": "json",
                "prop": "imageinfo",
                "titles": file_title,
                "iiprop": "url"
            }

            imageinfo_response = requests.get(search_url, params=imageinfo_params)
            imageinfo_response.raise_for_status()
            imageinfo_data = imageinfo_response.json()

            pages = imageinfo_data.get("query", {}).get("pages", {})
            for page in pages.values():
                imageinfo = page.get("imageinfo", [])
                if not imageinfo:
                    continue
                image_url = imageinfo[0].get("url")

                if image_url and image_url.lower().endswith((".jpg", ".jpeg", ".png")):
                    filename = file_title.replace("File:", "").replace(" ", "_")
                    save_name = f"{n}-commons-{filename}"
                    urllib.request.urlretrieve(image_url, save_name)
                    print(f"✅ {search_query} → {save_name}")
                    return save_name, image_url

        print(f"❌ Aucune image valide trouvée pour : {search_query}")
        return "", ""

    except Exception as e:
        print(f"[Erreur] {search_query} : {e}")
        return "", ""

import csv

# n = 0
# with open("_MASTER-All-20e.csv", newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         query = (row.get('\ufeffDénomination', '') + " " + row.get('Auteur', '')) .strip()
#         fetch_commons_image_multi(query, n)
#         n += 1


input_file = "_MASTER-_WIKIMEDIA.csv"
output_file = "output-1607.csv"

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["Wikimedia-file", "Wikimedia-url"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    n = 0
    for row in reader:
        query = (row.get('\ufeffDénomination', '') + " " + row.get('Auteur', '')) .strip()
        if not query:
            row["Wikimedia-file"] = ""
            row["Wikimedia-url"] = ""
        else:
            filename, image_url = fetch_commons_image_info(query, n)
            row["Wikimedia-file"] = filename
            row["Wikimedia-url"] = image_url
        writer.writerow(row)
        n += 1
