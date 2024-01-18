from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Lorsqu'on veut rediriger vers une page 404 quand une ressource
# est inexistante (remarque: au laboratoire cela ne fonctionnait pas
# parce que j'ai oublié de mettre le paramètre error dans la fonction
# page_not_found()
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def home():
    # Si le client envoie une requete GET, on affiche le formulaire
    if request.method == 'GET':
        return render_template('index.html'), 200
    # Sinon la méthode est POST, on récupère les informations entrées
    else:
        text = request.form['text']
        radio = request.form.get('radio')
        select = request.form.get('select')
        erreur = "Tous les champs du formulaire doivent être....."

        if text == "" or radio is None or select == "":
            # envoyer une variable interprétable par Jinja2
            return render_template("index.html", erreur=erreur, text=text), 400
        else:
            # Si valides, on écrit les informations récupérées dans le fichier log.txt
            log = open('log.txt','w')
            log.write("test %s " % text +
                      " \nradio %s " % radio + " \nselect %s" % select + "\n")
            log.close()

            #return redirect("/confirmation"), 302
            return redirect(url_for('confirmation'), 302)

@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html", title="page de confirmation"), 200