import json

# 1. Charger le fichier JSON
with open("data/content.json", "r") as f:
    contenus = json.load(f)

# 2. Afficher le nombre de cours
print(f"Il y a {len(contenus)} cours disponibles.")

# 3. Afficher les titres de tous les cours
print("\nTitres des cours :")
for cours in contenus:
    print(f"- {cours['title']}")

# 4. Filtrer les cours contenant le mot 'Python'
print("\nCours contenant 'Python' :")
for cours in contenus:
    if "Python" in cours["description"]:
        print(f"-> {cours['title']} : {cours['description']}")

# 5. Créer une liste des identifiants (IDs)
ids = [cours["id"] for cours in contenus]
print(f"\nListe des IDs : {ids}")
