class Utilisateur:
    def __init__(self, id, nom, prenom, age, date_naissance,
                 grades_universitaires):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.date_naissance = date_naissance
        self.grades_universitaires = grades_universitaires

    def set_id(self, id):
        self.id = id