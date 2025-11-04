Airtable : https://airtable.com/appsR54er8q9wjsqn/tblgtBkVl9fsJAPUq/viwOXSVHofLxtPI73?blocks=hide 


0. Dans _MASTER / vue “url-and-names” : convertir toutes les pièces jointes de la colonne “Image - pour validation” en URL en utilisant l’extension “Convert attachments to URL” (car sinon, celles-ci expirent d’un export à l’autre). Automatiquement la colonne “Fichier” sera remplie avec les noms des fichiers non vides si une URL existe a été extraite du champ “Image - pour validation”, sous la forme ID-HGAX-nom.

1. Exporter la table _MASTER, vue “url-and-names”, en csv 

2. Exporter la table  _MASTER, vue “POUR EXPORT”, en csv 

3. Exporter toutes les tables de liaisons, vues “Grid View”, en csv. Les placer toutes dans un même dossier appelé tables. 

4. Utiliser le script Python EXPORT-concat-tables-liaison.py pour additionner toutes les tables de liaison placées dans le dossier tables. -> La table de sortie sera LIAISON.csv

5. Utiliser le script Python EXPORT-airtable-download-url.py pour télécharger toutes les images à partir du csv url-and-names.csv. -> les images sont automatiquement téléchargées et rangées dans des dossiers par année, HGA1, HGA2 et HGA3.

6. Utiliser le script Python EXPORT-null-filler.py pour remplacer toutes les cellules vides de MASTER - VUE EXPORT.csv par “null” et insérer des espaces entre les tags des colonnes Matériaux et Techniques. Le fichier de sortie sera MASTER.csv.
Traiter toutes les images, par exemple avec l’outil XnConvert. 

Paramètres de conversion :
- taille : 2000 px max
- résolution : 144 DPI
- extension : jpg
	
7. Créer un dossier images. Exporter les images dans images/HGA1, images/HGA2, images/HGA3.


Structure finale de l’export : MASTER.csv, LIAISON.csv et le dossier images.
