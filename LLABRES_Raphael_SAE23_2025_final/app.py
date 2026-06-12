#!/usr/bin/env python3
import os
import db
import cherrypy

# Chemin absolu du dossier où se trouve app.py
# Permet de construire des chemins vers les templates et fichiers statiques
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Associe chaque race à ses deux photos (adulte, chiot)
# Permet d'afficher les bonnes images sans passer par la base de données
IMAGE_MAP = {
    "Berger Allemand":    ("berger-allemand.jpg",    "berger-allemand-chiot.jpg"),
    "Chihuahua":          ("chihuahua.jpg",           "chihuahua-chiot.jpg"),
    "Husky Sibérien":     ("husky-siberien.jpg",      "husky-siberien-chiot.jpg"),
    "Labrador Retriever": ("retriever.jpg",           "retriever-chiot.jpg"),
}

def render_template(template_name, context={}):
    """
    Charge un fichier HTML depuis le dossier templates et remplace
    les variables {{clé}} par les valeurs du dictionnaire context.
    Retourne le HTML final sous forme de chaîne de caractères.
    """
    path = os.path.join(CURRENT_DIR, "templates", template_name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for key, value in context.items():
        content = content.replace(f"{{{{{key}}}}}", str(value))
    return content

class DogPedia:

    @cherrypy.expose
    def index(self):
        """Redirige automatiquement la racine '/' vers la page d'accueil."""
        raise cherrypy.HTTPRedirect("/accueil")

    @cherrypy.expose
    def accueil(self, pseudo="Anonyme", mail="inconnu@mail.com", age=20, sexe="M", idRacePref=None):
        """
        Page d'accueil du site.
        - En POST : enregistre le vote de l'utilisateur dans la BDD puis redirige.
        - En GET  : affiche le formulaire de vote et le classement des races les plus votées.
        """
        # Traitement du formulaire de vote soumis par l'utilisateur
        if cherrypy.request.method == "POST" and idRacePref:
            try:
                # Ajout de l'utilisateur et enregistrement de son vote
                user_id = db.add_user(mail, int(age), sexe, pseudo, idRacePref)
                conn = db.get_connection()
                conn.execute("INSERT INTO VOTER (idUser, IdRace) VALUES (?, ?)", (user_id, idRacePref))
                conn.commit()
                conn.close()
            except Exception as e:
                print("Erreur lors du vote:", e)
            # Redirection pour éviter le renvoi du formulaire au rafraîchissement
            raise cherrypy.HTTPRedirect("/accueil")

        # Récupération du classement des 5 races les plus votées
        conn = db.get_connection()
        votes_data = conn.execute("""
            SELECT r.nomRace, COUNT(v.idUser) as total 
            FROM Race r LEFT JOIN VOTER v ON r.IdRace = v.IdRace 
            GROUP BY r.IdRace ORDER BY total DESC LIMIT 5
        """).fetchall()
        conn.close()

        # Construction du HTML pour le classement et les options du formulaire
        classement_html = "".join([f"<li><strong>{r['nomRace']}</strong> : {r['total']} vote(s)</li>" for r in votes_data])
        races = db.get_all_races()
        options_html = "".join([f"<option value='{r['IdRace']}'>{r['nomRace']}</option>" for r in races])
        
        return render_template("accueil.html", {"classement": classement_html, "options_races": options_html})

    @cherrypy.expose
    def races(self):
        """
        Page publique listant toutes les races de la BDD.
        Pour chaque race, génère une carte déroulante avec ses informations
        et un sélecteur de photo (adulte / chiot) via IMAGE_MAP.
        """
        races = db.get_all_races()
        races_html = ""
        for r in races:
            # Récupération des deux images associées à la race
            img1, img2 = IMAGE_MAP.get(r['nomRace'], ('default.jpg', 'default.jpg'))

            races_html += f"""
            <div class="race-card">
                <h3 class="race-title">{r['nomRace']}</h3>
                <div class="race-details">
                    <p><strong>Pays d'origine :</strong> {r['paysOrigine']}</p>
                    <p><strong>Taille Moyenne :</strong> {r['tailleMoy']} cm</p>
                    <p><strong>Durée de vie :</strong> {r['dureeVie']} ans</p>
                    <p><strong>Climat idéal :</strong> {r['climat']}</p>
                    <p><strong>Description :</strong> {r['description']}</p>
                    
                    <div class="photo-selector">
                        <label>Visionner la photo :</label>
                        <div class="photo-buttons">
                            <button onclick="showPhoto(this, '/static/images/{img1}')" class="photo-btn active">Adulte</button>
                            <button onclick="showPhoto(this, '/static/images/{img2}')" class="photo-btn">Chiot</button>
                        </div>
                        <div class="image-container">
                            <img src="/static/images/{img1}" class="zoomable-img" alt="{r['nomRace']}">
                        </div>
                    </div>
                </div>
            </div>
            """
        return render_template("principale.html", {"liste_races": races_html})

    @cherrypy.expose
    def admin(self, search=""):
        """
        Interface d'administration (backoffice).
        Affiche un graphique SVG des votes par race, un champ de recherche
        et le tableau CRUD complet des races de la BDD.
        Le paramètre 'search' filtre les races par nom si renseigné.
        """
        conn = db.get_connection()

        # Filtrage des races selon la recherche, ou récupération de toutes les races
        if search:
            races_list = conn.execute("SELECT * FROM Race WHERE nomRace LIKE ? ORDER BY nomRace ASC", (f"%{search}%",)).fetchall()
        else:
            races_list = conn.execute("SELECT * FROM Race ORDER BY nomRace ASC").fetchall()

        # Données pour le graphique : nombre de votes par race
        stats_data = conn.execute("""
            SELECT r.nomRace, COUNT(v.idUser) as total FROM Race r 
            LEFT JOIN VOTER v ON r.IdRace = v.IdRace GROUP BY r.IdRace
        """).fetchall()
        conn.close()
        
        # Construction du graphique en barres SVG
        svg_bars = ""
        x_offset = 60
        for stat in stats_data:
            height = min(stat['total'] * 30, 150)
            y_pos = 180 - height
            svg_bars += f"""
            <rect x="{x_offset}" y="{y_pos}" width="45" height="{height}" fill="#38bdf8" rx="4" />
            <text x="{x_offset + 22}" y="{y_pos - 8}" font-size="12" font-family="'Inter', sans-serif" font-weight="bold" fill="#f8fafc" text-anchor="middle">{stat['total']}</text>
            <text x="{x_offset + 22}" y="205" font-size="11" font-family="'Inter', sans-serif" font-weight="500" fill="#94a3b8" text-anchor="middle">{stat['nomRace']}</text>
            """
            x_offset += 100
            
        svg_chart = f'<svg width="100%" height="240" viewBox="0 0 800 240" style="background:#1e293b; border-radius:8px;">{svg_bars}</svg>'
        
        # Construction des lignes du tableau CRUD
        table_rows = ""
        for r in races_list:
            table_rows += f"""
            <tr>
                <td>{r['IdRace']}</td>
                <td><strong>{r['nomRace']}</strong></td>
                <td>{r['paysOrigine']}</td>
                <td>{r['tailleMoy']} cm</td>
                <td>
                    <a href="/admin/edit?id={r['IdRace']}" class="btn-edit">Modifier</a> | 
                    <a href="/admin/delete?id={r['IdRace']}" class="btn-delete" onclick="return confirm('Supprimer cette race ?')">Supprimer</a>
                </td>
            </tr>
            """
        return render_template("admin.html", {"crud_table": table_rows, "chart_svg": svg_chart, "search_value": search})

    @cherrypy.expose
    def admin_add(self, nomRace="", tailleMoy=0, dureeVie=0, paysOrigine="", climat="", description=""):
        """
        Reçoit les données du formulaire d'ajout et insère une nouvelle race
        dans la BDD via db.add_race(), puis redirige vers l'admin.
        """
        try:
            db.add_race(nomRace, float(tailleMoy or 0), int(dureeVie or 0), paysOrigine, climat, description)
        except Exception as e:
            print("Erreur lors de l'ajout de la race :", e)
        raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose
    def admin_edit(self, id, nomRace=None, tailleMoy=0, dureeVie=0, paysOrigine="", climat="", description=""):
        """
        Affiche le formulaire de modification d'une race (GET)
        et enregistre les modifications dans la BDD (POST).
        Redirige vers l'admin si la race n'existe pas.
        """
        race = db.get_race_by_id(id)
        if not race:
            raise cherrypy.HTTPRedirect("/admin")
            
        if cherrypy.request.method == "POST":
            # Mise à jour de la race avec les nouvelles valeurs du formulaire
            db.update_race(id, nomRace, float(tailleMoy or 0), int(dureeVie or 0), paysOrigine, climat, description)
            raise cherrypy.HTTPRedirect("/admin")

        # Affichage du formulaire pré-rempli avec les valeurs actuelles
        return render_template("admin_edit.html", {
            "id": race["IdRace"], "nom": race["nomRace"], "taille": race["tailleMoy"],
            "vie": race["dureeVie"], "pays": race["paysOrigine"], "climat": race["climat"], "desc": race["description"]
        })

    @cherrypy.expose
    def admin_delete(self, id=None):
        """
        Supprime la race correspondant à l'id passé en paramètre
        via db.delete_race(), puis redirige vers l'admin.
        """
        if id:
            db.delete_race(id)
        raise cherrypy.HTTPRedirect("/admin")


# --- CONFIGURATION ET LANCEMENT DE CHERRYPY ---
if __name__ == "__main__":
    config = {
        '/': {
            'tools.sessions.on': True,
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8',
        },
        # Sert les fichiers statiques (CSS, JS, images, fonts) depuis le dossier /static
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(CURRENT_DIR, 'static')
        }
    }
    
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080
    })
    
    print("Le serveur CherryPy tourne sur http://127.0.0.1:8080")
    cherrypy.quickstart(DogPedia(), '/', config)