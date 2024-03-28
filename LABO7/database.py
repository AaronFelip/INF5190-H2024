import sqlite3


class Database():

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def add_person(self, nom, sex, age, ville):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO personne(nom, sex, age, ville)" "VALUES(?, ?, ?, ?)",
            (nom, sex, age, ville))
        connection.commit()

    def get_all_persons(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM personne")
        persons = cursor.fetchall()
        return persons

    def get_person_by_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM personne WHERE id=%d" % id)
        infos = cursor.fetchall()
        return infos