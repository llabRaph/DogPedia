# DogPedia - Dog Breed Encyclopedia

A web application built with CherryPy and SQLite that allows users to explore dog breeds, vote for their favourite, and manage the database through an admin interface.

---

## Project Overview

DogPedia is a dog breed encyclopedia where:
- **Public users** can browse all dog breeds, view their characteristics and photos (adult & puppy), and vote for their favourite breed.
- **Administrators** can create, read, update, and delete breeds via a backoffice interface with search and statistics.

---

## Python Dependencies

- Python 3.x
- CherryPy

Install with:
```
pip install cherrypy
```

---

## Project Structure

```
LLABRES_Raphael_SAE_2025_final/
├── app.py              # CherryPy web server
├── db.py               # Database access layer
├── CLI.py              # Command-line interface
├── create_db.py        # Script to create the database and tables
├── insert_test.py      # Script to insert test data
├── schema.sql          # SQL schema dump
├── SAE23.db            # SQLite database (auto-generated)
├── static/
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript
│   ├── images/         # Dog breed photos
│   └── fonts/          # Inter font files (.ttf)
└── templates/          # HTML templates
```

---

## Installation

**1. Clone or extract the project**
```
cd LLABRES_Raphael_SAE_2025_final
```

**2. Install the dependency**
```
pip install cherrypy
```

**3. Initialize the database**
```
python3 create_db.py
```

**3.2 Initialize the database**
```
If there is no data you have to write this command in your terminal
python3 insert_test.py
```

**4. Start the web server**
```
python3 app.py
```

---

## URLs

| Interface  | URL                           |
|------------|-------------------------------|
| Home page  | http://127.0.0.1:8080/accueil |
| Breed list | http://127.0.0.1:8080/races   |
| Admin      | http://127.0.0.1:8080/admin   |

---

## CLI Usage

Launch the CLI tool:
```
python3 CLI.py
```

**Example 1 — List all breeds**
```
=== MENU PRINCIPAL ===
  1. Gérer les races
  2. Gérer les utilisateurs
  0. Quitter
Votre choix : 1

=== GESTION DES RACES ===
  1. Lister toutes les races
  ...
Votre choix : 1

  ID         Nom                  Taille   Durée vie  Pays            Climat
  -------------------------------------------------------------------------------------
  kf88ckw    Berger Allemand      63.0     11         Allemagne       Tempéré
  kl471kp    Chihuahua            20.0     15         Mexique         Chaud
  rh8d5tx    Husky Sibérien       58.0     13         Russie          Froid
  psgwgpq    Labrador Retriever   57.0     12         Canada          Tempéré
```

**Example 2 — Add a new breed**
```
Votre choix : 3

--- Nouvelle race ---
Nom           : Dalmatien
Taille moy(cm): 55
Durée vie(ans): 13
Pays d'origine: Croatie
Climat        : Tempéré
Description   : Chien à taches noires et blanches.

  Race ajoutée avec l'ID : x7k29mq
```

---

## Database Initialization

The database uses SQLite and contains 3 tables:

- **Race** — stores breed information (name, size, lifespan, country, climate, description)
- **Utilisateur** — stores user information (email, age, gender, username, preferred breed)
- **VOTER** — junction table linking users to their voted breed

To reset the database from scratch:
```
python3 delete_db.py
python3 create_db.py
python3 insert_test.py
```
