import json


with open("data/content.json", "r") as f:
    cours_disponibles = json.load(f)

print ("Voici la liste des cours: ")
for cours in cours_disponibles:
    print(f"[{cours['id']}] {cours['title']}")

choix=input("Quel cours voulez-vous marquer comme 'préféfré ? (Entrez un ID) :")

try:
    choix_id=int(choix)
    cours_choisi= next((c for c in  cours_disponibles if c['id']==choix_id),None)

    if cours_choisi:
        print(f"Vous aveez choisi le cour :{cours_choisi['title']}")

        interaction={
            "user_id":1,
            "course_id":cours_choisi["id"],
            "action":"like"
        }

        with open("data/interactions.json","w") as f:
            json.dump(interaction,f,indent=2)

        print =("Interaction enregistrée dans la data/interactions.json")
    else:
        print("ID non trouvé.")

except ValueError:
    print("vueillez entrez un chiffre valide.")