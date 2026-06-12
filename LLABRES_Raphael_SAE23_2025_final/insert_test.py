# insert_test.py
import db

def insert_test_data():
    print("Insertion des données de test...")

    # 1. Insertion des Races et récupération de leurs IDs générés aléatoirement
    id_labrador = db.add_race("Labrador Retriever", 57.0, 12, "Canada", "Tempéré", "Chien de famille.")
    id_husky    = db.add_race("Husky Sibérien",     58.0, 13, "Russie",  "Froid",    "Chien de traîneau.")
    id_chihuahua = db.add_race("Chihuahua",          20.0, 15, "Mexique", "Chaud",    "Petit chien.")
    id_berger    = db.add_race("Berger Allemand",    63.0, 11, "Allemagne","Tempéré", "Chien de travail.")

    # 2. Insertion des Utilisateurs en utilisant les IDs de races récupérés ci-dessus
    db.add_user("alice@mail.com", 25, "F", "Alice",  id_labrador)
    db.add_user("bob@mail.com",   30, "M", "Bob",    id_husky)
    db.add_user("carol@mail.com", 22, "F", "Carol",  id_chihuahua)
    db.add_user("dave@mail.com",  28, "M", "Dave",   None)

    print("Données de test insérées avec succès.")

if __name__ == "__main__":
    insert_test_data()