#!/usr/bin/env python3
import os

DB_PATH = "SAE23.db"

def delete_database(): #supprime la base de données
    if os.path.exists(DB_PATH): #si le fichier a un chemin existant, alors
        os.remove(DB_PATH) # on supprime le fichier
        print(f"'{DB_PATH}' supprimée.")
    else:
        print(f"Aucune base existante trouvée.")

if __name__ == "__main__":
    confirm = input("Toutes les données seront perdues. Confirmer ? (o/n) : ")
    if confirm.lower() == "o":
        delete_database()
    else:
        print("Annulé.")