# cli.py

import db

# ─── Affichage ─────────────────────────────────────────

def print_races(races):
    if not races:
        print("  (aucune race)")
        return
    print(f"  {'ID':<10} {'Nom':<20} {'Taille':<8} {'Durée vie':<10} {'Pays':<15} {'Climat'}")
    print("  " + "-"*85)
    for r in races:
        print(f"  {str(r['IdRace']):<10} {r['nomRace']:<20} {r['tailleMoy']:<8} {r['dureeVie']:<10} {r['paysOrigine']:<15} {r['climat']}")

def print_users(users):
    if not users:
        print("  (aucun utilisateur)")
        return
    print(f"  {'ID':<10} {'Pseudo':<15} {'Mail':<25} {'Age':<5} {'Sexe':<6} {'Race préf.'}")
    print("  " + "-"*85)
    for u in users:
        race_pref = u['idRacePref'] if u['idRacePref'] else "Aucune"
        print(f"  {str(u['idUser']):<10} {str(u['pseudo']):<15} {u['mail']:<25} {str(u['age']):<5} {str(u['sexe']):<6} {str(race_pref)}")

# ─── Menus RACE ────────────────────────────────────────

def menu_races():
    while True:
        print("\n=== GESTION DES RACES ===")
        print("  1. Lister toutes les races")
        print("  2. Voir une race (par ID)")
        print("  3. Ajouter une race")
        print("  4. Modifier une race")
        print("  5. Supprimer une race")
        print("  0. Retour")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            races = db.get_all_races()
            print_races(races)

        elif choix == "2":
            id_race = input("ID de la race (ex: a1b2c3d) : ").strip()
            r = db.get_race_by_id(id_race)
            if r:
                for key in r.keys():
                    print(f"  {key}: {r[key]}")
            else:
                print("  Race introuvable.")

        elif choix == "3":
            print("--- Nouvelle race ---")
            nom     = input("Nom           : ")
            taille  = input("Taille moy(cm): ")
            duree   = input("Durée vie(ans): ")
            pays    = input("Pays d'origine: ")
            climat  = input("Climat        : ")
            desc    = input("Description   : ")
            new_id = db.add_race(nom, float(taille or 0), int(duree or 0), pays, climat, desc)
            print(f"  Race ajoutée avec l'ID : {new_id}")

        elif choix == "4":
            id_race = input("ID de la race à modifier : ").strip()
            r = db.get_race_by_id(id_race)
            if not r:
                print("  Race introuvable.")
                continue
            print("  (Appuyez sur Entrée pour garder la valeur actuelle)")
            nom    = input(f"  Nom [{r['nomRace']}]       : ") or r['nomRace']
            taille = input(f"  Taille [{r['tailleMoy']}]  : ") or r['tailleMoy']
            duree  = input(f"  Durée [{r['dureeVie']}]    : ") or r['dureeVie']
            pays   = input(f"  Pays [{r['paysOrigine']}]  : ") or r['paysOrigine']
            climat = input(f"  Climat [{r['climat']}]     : ") or r['climat']
            desc   = input(f"  Desc [{r['description']}]  : ") or r['description']
            db.update_race(id_race, nom, float(taille), int(duree), pays, climat, desc)
            print("  Race mise à jour.")

        elif choix == "5":
            id_race = input("ID de la race à supprimer : ").strip()
            confirm = input(f"Confirmer suppression de la race {id_race} ? (o/n) : ")
            if confirm.lower() == "o":
                db.delete_race(id_race)
                print("Race supprimée.")

        elif choix == "0":
            break

# ─── Menus UTILISATEUR ─────────────────────────────────

def menu_users():
    while True:
        print("\n=== GESTION DES UTILISATEURS ===")
        print("  1. Lister tous les utilisateurs")
        print("  2. Voir un utilisateur (par ID)")
        print("  3. Ajouter un utilisateur")
        print("  4. Modifier un utilisateur")
        print("  5. Supprimer un utilisateur")
        print("  0. Retour")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            users = db.get_all_users()
            print_users(users)

        elif choix == "2":
            id_user = input("ID de l'utilisateur : ").strip()
            u = db.get_user_by_id(id_user)
            if u:
                for key in u.keys():
                    print(f"  {key}: {u[key]}")
            else:
                print("  Utilisateur introuvable.")

        elif choix == "3":
            print("--- Nouvel utilisateur ---")
            mail   = input("Mail    : ")
            age    = input("Age     : ")
            sexe   = input("Sexe (M/F/Autre) : ")
            pseudo = input("Pseudo  : ")
            pref   = input("ID race préférée (ex: a1b2c3d, ou vide) : ").strip()
            db.add_user(mail, int(age or 0), sexe, pseudo, pref if pref else None)
            print("  Utilisateur ajouté.")

        elif choix == "4":
            id_user = input("ID de l'utilisateur à modifier : ").strip()
            u = db.get_user_by_id(id_user)
            if not u:
                print("  Utilisateur introuvable.")
                continue
            print("  (Appuyez sur Entrée pour garder la valeur actuelle)")
            mail   = input(f"  Mail [{u['mail']}]    : ") or u['mail']
            age    = input(f"  Age [{u['age']}]      : ") or u['age']
            sexe   = input(f"  Sexe [{u['sexe']}]    : ") or u['sexe']
            pseudo = input(f"  Pseudo [{u['pseudo']}]: ") or u['pseudo']
            pref   = input(f"  Race préf [{u['idRacePref']}]: ").strip()
            new_pref = pref if pref else u['idRacePref']
            db.update_user(id_user, mail, int(age), sexe, pseudo, new_pref)
            print("  Utilisateur mis à jour.")

        elif choix == "5":
            id_user = input("ID de l'utilisateur à supprimer : ").strip()
            confirm = input(f"Confirmer suppression de l'utilisateur {id_user} ? (o/n) : ")
            if confirm.lower() == "o":
                db.delete_user(id_user)
                print("  Utilisateur supprimé.")

        elif choix == "0":
            break

# ─── Menu principal ────────────────────────────────────

def main():
    print("╔══════════════════════════════╗")
    print("║   SAE23 - Administration CLI ║")
    print("╚══════════════════════════════╝")
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("  1. Gérer les races")
        print("  2. Gérer les utilisateurs")
        print("  0. Quitter")
        choix = input("Votre choix : ").strip()
        if choix == "1":
            menu_races()
        elif choix == "2":
            menu_users()
        elif choix == "0":
            print("Au revoir.")
            break

if __name__ == "__main__":
    main()