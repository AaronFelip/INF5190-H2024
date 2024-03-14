from flask import Flask, render_template, request, g, jsonify
from flask_json_schema import JsonValidationError, JsonSchema
from schema import (valider_nouvel_utilisateur_schema,
                    modifier_utilisateur_schema)
from database import Database
from utilisateur import Utilisateur

app = Flask(__name__)
schema = JsonSchema(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400


@app.route('/api/utilisateur', methods=['POST'])
@schema.validate(valider_nouvel_utilisateur_schema)
def utilisateur():
    try:
        data = request.get_json()
        nouvel_utilisateur = Utilisateur(None, data["nom"], data["prenom"],
                                         data["age"],
                                         data["date_naissance"],
                                         data["grades_universitaires"])
        get_db().creer_utilisateur(nouvel_utilisateur)

        """
        201 Created : Ce code est renvoyé lorsqu'une nouvelle ressource a été 
        créée avec succès.
        """
        return ("L'utilisateur " + data["prenom"] + " " +
                    data["nom"] + " a été ajouté avec succès.", 201)

    except Exception as e:
        return jsonify(error="Une erreur interne s'est produite. L'erreur a été "
                             "signalée à l'équipe de développement."), 500


@app.route('/api/utilisateur/<int:id>', methods=['PUT'])
@schema.validate(modifier_utilisateur_schema)
def modifier_utilisateur(id):
    try:
        data = request.get_json()

        """
        Ici on utilisera data.get() pour qu'elle ne s'attende pas à ce que tous 
        les champs soient toujours présents dans la requête.
        """
        utilisateur_modifie = Utilisateur(id,
                                          data.get("nom"),
                                          data.get("prenom"),
                                          data.get("age"),
                                          data.get("date_naissance"),
                                          data.get("grades_universitaires"))

        resultat = get_db().modifier_utilisateur(utilisateur_modifie)

        if resultat:
            return jsonify(message=f"L'utilisateur avec l'id: {id} a été modifié avec succès."), 200
        else:
            return jsonify(error=f"Utilisateur non trouvé avec l'id spécifié: {id}."), 404

    except Exception as e:
        return jsonify(error="Une erreur interne s'est produite. L'erreur a été "
                             "signalée à l'équipe de développement."), 500



@app.route('/api/utilisateurs', methods=['GET'])
def obtenir_utilisateurs():
    utilisateurs = get_db().obtenir_tous_les_utilisateurs()
    utilisateurs_json = [{"id": user.id, "nom": user.nom, "prenom": user.prenom, "age": user.age, "date_naissance": user.date_naissance, "grades_universitaires": user.grades_universitaires} for user in utilisateurs]
    return jsonify(utilisateurs_json)


@app.route('/doc')
def doc():
    return render_template("doc.html")


if __name__ == '__main__':
    app.run()
