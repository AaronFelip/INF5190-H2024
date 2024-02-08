from flask import Flask, render_template, session, redirect, url_for, g, request, flash
from authlib.integrations.flask_client import OAuth #pip install authlib et pip install requests
from datetime import timedelta
import os
from authorization_decorator import login_required

# Nous nous servirons de dotenv pour importer des variables d'environnement
from dotenv import load_dotenv #pip install python-dotenv
load_dotenv()

# TODO 0: Créer des variables secrète pour gérer les sessions, ce serait une très mauvaise
#  pratique de déclarer les constantes ici, principalement à cause des petits malins qui les
#  récupéreront sur des plateformes tel que GitHub.

"""
Étape 1: créez un fichier .env à la racine de votre projet, ajouter ce fichier sur .gitignore
Étape 2: créez les variables suivantes:
APP_SECRET_KEY=secrets.token_hex(16)
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
APP_SESSION_COOKIE_NAME=myapp_session
PERMANENT_SESSION_LIFETIME=1

pour les variables google, il faudra avoir en main un compte google puis d'accéder à
Google cloud console. Voir la démonstration.

👉 URI de redirection: http://127.0.0.1:5000/authorize

Pour des raisons de sécurité, vous ne pouvez pas utiliser les miennes.
NE LES PARTAGEZ PAS, SURTOUT PAS!!!
Attention, si vous les partagez avec une tierce personne, cette personne pourrait
se servir de votre compte google pour commettre des méfaits!
"""


app = Flask(__name__, static_url_path="", static_folder="static")

session_lifetime_days = int(os.getenv("PERMANENT_SESSION_LIFETIME", 7))
app.secret_key = os.getenv("APP_SECRET_KEY")
app.session_cookie_name = os.getenv("APP_SESSION_COOKIE_NAME")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=session_lifetime_days)

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    userinfo_endpoint="https://www.googleapis.com/oauth2/v3/userinfo",
    client_kwargs={"scope": "openid email profile"},
)

# TODO 1: faire la connection et déconnection de la base de donnée (voir labo précédent)


@app.route("/")
@login_required
def home():
    # Vous permet simplement de vous assurer que vos variables de session
    # sont bien initiliasé avant de passé à la prochaine étape
    page_1_checked = session.get("page_1_checked")
    page_2_checked = session.get("page_2_checked")
    page_3_checked = session.get("page_3_checked")
    return render_template("index.html", page_1_checked=page_1_checked,
                           page_2_checked=page_2_checked,page_3_checked=page_3_checked), 200


@app.route("/login")
def login():
    google = oauth.create_client('google')
    redirect_url = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_url)

@app.route("/authorize")
def authorize():
    # Par pitié, veuillez lire la documentation :(
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get("https://www.googleapis.com/oauth2/v3/userinfo")
    user_info = resp.json()
    session["profile"] = user_info
    session["page"] = 1
    session["page_1_checked"] = True
    session.permanent = False

    print (user_info) # ceci vous permettera de voir dans la console les informations venant de google
    return redirect("/")


@app.route("/page1", methods=["GET", "POST"])
@login_required
def page1():
    if session["page"] != 1:
        return render_template("page1.html"), 200
    else:
        if request.method == "GET":
            return render_template("page1.html"), 200
        else:
            nom = request.form["nom"]
            prenom = request.form["prenom"]
            ville = request.form["ville"]
            # TODO 2: gérer les erreurs, sinon vos clés de session seront vide et retourner l'utilisateur
            #  à la page 1 si le formulaire est incomplet! N'oubliez de corriger la page html en questio
            #  de manière a ce que l'utilisateur n'ai pas en fournir une seconde fois des inputs déjà saisi
            
            session["nom"] = nom
            session["prenom"] = prenom
            session["ville"] = ville
            session["page"] = 2
            session["page_2_checked"] = True
            return redirect("/page2")


@app.route("/page2", methods=["GET", "POST"])
@login_required
def page2():
    if session["page"] != 2:
        return render_template("acces-non-authorise.html"), 200
    else:
        if request.method == "GET":
            email = dict(session)["profile"]["email"]
            nom = session["nom"]
            prenom = session["prenom"]
            ville = session["ville"]

            return render_template("page2.html",
                                   email=email,nom=nom,prenom=prenom,ville=ville )
        else:
            if request.form.get("valide"):
                session["page"] = 3
                session["page_3_checked"] = True
                return redirect("/page3"), 302
            else:
                # utilisation de flash pour afficher un message d'erreur
                flash("Il y a une erreur!")
                return redirect("/page2"), 302


@app.route("/page3", methods=["GET", "POST"])
@login_required
def page3():
    if session["page"] != 3:
        return render_template("acces-non-authorise.html"), 200
    else:
        if request.method == "GET":
            return render_template("page3.html")
        else:
            enfant = request.form.get("enfant")
            session["enfant"] = enfant
            # TODO 3: enregistrer dans la base de données en utilisant tout
            #  ce qui a été stocker dans la session. Bien évidemment, il faut
            #  créer une base de données, charger les tables et tout le kit, tsé!

            return redirect("/confirmation"), 302


@app.route("/confirmation")
@login_required
def confirmation():
    name = session["prenom"]
    return render_template("confirmation.html", name=name), 200

@app.route("/logout")
def logout():
    # Efface toutes les données de la session
    session.clear()

    """
    Vous auriez pu faire aussi:
    
    for key in list(session.keys()):
        session.pop(key)
        
    Mais moins cool!    
    """

    return redirect("/"), 302


# TODO 4: faire la route de gestion des pages 404
# TODO 5: valider votre code python avec pycodestyle
# TODO 6: payer un café au démonstrateur

