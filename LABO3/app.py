from flask import Flask, render_template, redirect, request
#from database import Database
from datetime import datetime
import re
import hashlib
import uuid

app = Flask(__name__, static_url_path="", static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def index():

    title = "Pismoé - veuillez vous inscrire"

    if request.method == 'GET':
        return render_template('index.html', title=title), 200
    else:
        nom = request.form['nom']
        prenom = request.form['prenom']
        courriel = request.form['courriel']
        validation_courriel = request.form['validation-courriel']
        mdp = request.form['mdp']

        if nom == "" or prenom == "" or courriel == "" or validation_courriel == "" or mdp == "":
            message_erreur = "Erreur, tous les champs doivent être remplis"
            return render_template("index.html", title= title, nom=nom, prenom=prenom,
                                   courriel=courriel, message_erreur=message_erreur), 400

        if courriel_existe(courriel):
            courriel_erreur = "Ce courriel existe deja"
            return render_template("index.html", title=title, nom=nom, prenom=prenom, courriel_erreur=courriel_erreur)