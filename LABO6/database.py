import sqlite3
import json
from utilisateur import Utilisateur


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/data.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def creer_utilisateur(self, utilisateur):
        connection = self.get_connection()
        cursor = connection.cursor()
        grades_json = json.dumps(utilisateur.grades_universitaires)

        cursor.execute(
            "INSERT INTO utilisateur (nom, prenom, age, "
            "date_naissance, grades_universitaires) VALUES (?, ?, ?, ?, ?)",
            (utilisateur.nom, utilisateur.prenom, utilisateur.age,
             utilisateur.date_naissance, grades_json))
        connection.commit()

    def modifier_utilisateur(self, utilisateur):
        connection = self.get_connection()
        cursor = connection.cursor()
        grades_json = json.dumps(
            utilisateur.grades_universitaires) if utilisateur.grades_universitaires else None

        champs_a_modifier = []
        valeurs_a_utiliser = []

        if utilisateur.nom:
            champs_a_modifier.append("nom = ?")
            valeurs_a_utiliser.append(utilisateur.nom)
        if utilisateur.prenom:
            champs_a_modifier.append("prenom = ?")
            valeurs_a_utiliser.append(utilisateur.prenom)
        if utilisateur.age is not None:  # Permet de gérer l'âge à 0
            champs_a_modifier.append("age = ?")
            valeurs_a_utiliser.append(utilisateur.age)
        if utilisateur.date_naissance:
            champs_a_modifier.append("date_naissance = ?")
            valeurs_a_utiliser.append(utilisateur.date_naissance)
        if grades_json:  # On vérifie si la liste est non vide ou non None
            champs_a_modifier.append("grades_universitaires = ?")
            valeurs_a_utiliser.append(grades_json)

        # Construire la requête SQL de mise à jour
        sql = "UPDATE utilisateur SET " + ", ".join(
            champs_a_modifier) + " WHERE id = ?"
        valeurs_a_utiliser.append(utilisateur.id)

        cursor.execute(sql, valeurs_a_utiliser)
        connection.commit()

        if cursor.rowcount == 0:
            return False
        else:
            return True


    def obtenir_tous_les_utilisateurs(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, nom, prenom, age, date_naissance, grades_universitaires FROM utilisateur"
        )

        utilisateurs = []
        for row in cursor.fetchall():
            id, nom, prenom, age, date_naissance, grades_json = row
            grades_universitaires = json.loads(grades_json) if grades_json else []
            utilisateur = Utilisateur(id, nom, prenom, age, date_naissance,
                                      grades_universitaires)
            utilisateurs.append(utilisateur)

        return utilisateurs
