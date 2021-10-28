# Bibliothèques
import sqlite3
import csv


def nomToJpg(nom):
    """
    convertir le nom en nom de chemin de fichier
    """
    future_nom = ""
    # chaque lettre du nom
    for lettre in nom[2:].strip():
        # convertir certaines lettres spéciales en caractères ascii
        if lettre == " ":
            lettre = "_"
        if lettre == "é":
            lettre = "e"
        if lettre == "î":
            lettre = "i"
        # convertir chaque lettre en minuscule
        future_nom += lettre.lower()
    # ajouter l'extension .jpg à notre nom
    future_nom += ".jpg"
    # renvoyer la valeur
    return future_nom


# connexion a la base de données
conn = sqlite3.connect("database.db")
# positionner le curseur
cur = conn.cursor()
# supprimer la table si elle existe déjà
cur.execute("DROP TABLE IF EXISTS main")
# création de la table 'main'
cur.execute("CREATE TABLE main (id INTEGER, nom TEXT, longueur_moy TEXT, longueur_max TEXT, poids_moy TEXT, poids_max TEXT, age_max TEXT, nourriture TEXT, emplacement TEXT, profondeur_min TEXT, profondeur_max TEXT, cause TEXT, reputation TEXT, description TEXT, protection TEXT, image_path TEXT, PRIMARY KEY(id))")

# on ouvre le fichier en mode lecture
with open("database.csv", "r") as file:
    # on récupère les valeurs sous forme de dictionnaire de file
    data = csv.DictReader(file)
    # 2D liste avec toutes les données
    allData = []
    # chaque ligne du fichier
    for e, row in enumerate(data):
        # initialisation d'une liste qui contiendra toutes les données
        rowInfo = []
        # récupérer les valeurs de chaque catégorie
        for values in row.values():
            # ajout des valeurs dans rowInfo
            rowInfo.append(values)
        # ajouter le nom du fichier dans rowInfo
        rowInfo.append(nomToJpg(rowInfo[1]))
        # ajouter rowInfo dans allData (sauvegarde de chaque ligne)
        allData.append(rowInfo)
        # inserer les lignes dans la base de données
        cur.execute("INSERT INTO main (id, nom, longueur_moy, longueur_max, poids_moy, poids_max, age_max, nourriture, emplacement, profondeur_min, profondeur_max, cause, reputation, description, protection, image_path) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (allData[e][0], allData[e][1], allData[e][2], allData[e][3], allData[e][4], allData[e][5], allData[e][6], allData[e][7], allData[e][8], allData[e][9], allData[e][10], allData[e][11], allData[e][12], allData[e][13], allData[e][14], allData[e][15]))
# commit les changements
conn.commit()
# fermer la connexion
conn.close()