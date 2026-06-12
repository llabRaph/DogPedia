#!/usr/bin/env python3
import sqlite3
import random
import string

DB_PATH = "SAE23.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ─── GÉNÉRATION D'ID (Format Alphanumérique 7 caractères) ───

def generate_id(table, id_column):
    conn = get_connection()
    characters = string.ascii_lowercase + string.digits
    while True:
        new_id = ''.join(random.choices(characters, k=7))
        exists = conn.execute(
            f"SELECT 1 FROM {table} WHERE {id_column} = ?", (new_id,)
        ).fetchone()
        if not exists:
            conn.close()
            return new_id

# ─── GESTION DES RACES ──────────────────────────────────────

def get_all_races():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM Race ORDER BY nomRace ASC").fetchall()
    conn.close()
    return rows

def get_race_by_id(id_race):
    conn = get_connection()
    row = conn.execute("SELECT * FROM Race WHERE IdRace = ?", (id_race,)).fetchone()
    conn.close()
    return row

def add_race(nomRace, tailleMoy, dureeVie, paysOrigine, climat, description):
    id_race = generate_id("Race", "IdRace")
    conn = get_connection()
    conn.execute("""
        INSERT INTO Race (IdRace, nomRace, tailleMoy, dureeVie, paysOrigine, climat, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_race, nomRace, tailleMoy, dureeVie, paysOrigine, climat, description))
    conn.commit()
    conn.close()
    return id_race

def update_race(id_race, nomRace, tailleMoy, dureeVie, paysOrigine, climat, description):
    conn = get_connection()
    conn.execute("""
        UPDATE Race SET nomRace=?, tailleMoy=?, dureeVie=?, paysOrigine=?, climat=?, description=?
        WHERE IdRace=?
    """, (nomRace, tailleMoy, dureeVie, paysOrigine, climat, description, id_race))
    conn.commit()
    conn.close()

def delete_race(id_race):
    conn = get_connection()
    conn.execute("DELETE FROM VOTER WHERE IdRace=?", (id_race,))
    conn.execute("UPDATE Utilisateur SET idRacePref=NULL WHERE idRacePref=?", (id_race,))
    conn.execute("DELETE FROM Race WHERE IdRace=?", (id_race,))
    conn.commit()
    conn.close()

# ─── GESTION DES UTILISATEURS ───────────────────────────────

def get_all_users():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM Utilisateur").fetchall()
    conn.close()
    return rows

def get_user_by_id(id_user):
    conn = get_connection()
    row = conn.execute("SELECT * FROM Utilisateur WHERE idUser=?", (id_user,)).fetchone()
    conn.close()
    return row

def add_user(mail, age, sexe, pseudo, idRacePref=None):
    id_user = generate_id("Utilisateur", "idUser")
    conn = get_connection()
    conn.execute("""
        INSERT INTO Utilisateur (idUser, mail, age, sexe, pseudo, idRacePref)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_user, mail, age, sexe, pseudo, idRacePref))
    conn.commit()
    conn.close()
    return id_user

def update_user(id_user, mail, age, sexe, pseudo, idRacePref):
    conn = get_connection()
    conn.execute("""
        UPDATE Utilisateur SET mail=?, age=?, sexe=?, pseudo=?, idRacePref=?
        WHERE idUser=?
    """, (mail, age, sexe, pseudo, idRacePref, id_user))
    conn.commit()
    conn.close()

def delete_user(id_user):
    conn = get_connection()
    conn.execute("DELETE FROM VOTER WHERE idUser=?", (id_user,))
    conn.execute("DELETE FROM Utilisateur WHERE idUser=?", (id_user,))
    conn.commit()
    conn.close()
    
# ─── VOTES ──────────────────────────────────────────────────

def get_classement_votes():
    conn = get_connection()
    rows = conn.execute("""
        SELECT Race.IdRace, Race.nomRace, COUNT(VOTER.idUser) as nb_votes
        FROM Race
        LEFT JOIN VOTER ON Race.IdRace = VOTER.IdRace
        GROUP BY Race.IdRace
        ORDER BY nb_votes DESC
    """).fetchall()
    conn.close()
    return rows

def add_vote(id_user, id_race):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO VOTER (idUser, IdRace) VALUES (?, ?)", (id_user, id_race))
    conn.commit()
    conn.close()

# ─── RECHERCHE ───────────────────────────────────────────────

def search_races(q):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM Race
        WHERE nomRace LIKE ? OR paysOrigine LIKE ? OR climat LIKE ?
        ORDER BY nomRace ASC
    """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
    conn.close()
    return rows

def get_races_par_pays():
    conn = get_connection()
    rows = conn.execute("""
        SELECT paysOrigine, COUNT(*) as nb_races
        FROM Race
        GROUP BY paysOrigine
        ORDER BY nb_races DESC
    """).fetchall()
    conn.close()
    return rows

def get_user_by_pseudo(pseudo):
    conn = get_connection()
    row = conn.execute("SELECT * FROM Utilisateur WHERE pseudo=?", (pseudo,)).fetchone()
    conn.close()
    return row

def get_stats_races():
    """Compte le nombre de chiens pour chaque race (pour le graphique)"""
    conn = sqlite3.connect("SAE23.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # On fait une jointure pour avoir le vrai nom de la race
    cursor.execute("""
        SELECT r.nom AS race_nom, COUNT(d.id) AS total 
        FROM races r
        LEFT JOIN chiens d ON d.race_id = r.id
        GROUP BY r.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows