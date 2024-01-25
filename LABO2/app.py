from flask import Flask, redirect, request, render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template("formulaire.html"), 200


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('formulaire.html'), 200
    else:
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']

        if nom == '' or prenom == '' or age == '':
            erreur = 'Tous les champs doivent être remplis'
            return render_template("formulaire.html",
                                   erreur=erreur, nom=nom, prenom=prenom, age=age)







        else:
            log = open("log.txt", 'a', encoding="utf8")
            log.write(nom + ", " + prenom + ", " + age + "\n")
            log.close()

            return redirect("/liste"), 302





@app.route('/liste')
def liste():
    resultats = []

    log = open("log.txt", 'r', encoding="utf8")
    lignes = log.readlines()
    log.close()

    for ligne in lignes:
        decouper = ligne.split(", ")
        resultats.append(decouper)

    return render_template("liste.html",
                           resultats=resultats, len=len(resultats))













