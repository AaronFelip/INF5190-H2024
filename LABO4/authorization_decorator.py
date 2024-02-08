from flask import session, render_template
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Décorateur qui vérifie si l'utilisateur est connecté en vérifiant si le
        nom complet de l'utilisateur est dans la session. Si l'utilisateur est
        connecté, la fonction décorée est appelée normalement.
        Sinon, retourne la page indiquant qu'il doit etre connecté pour visiter
        cettr page

        :return: fonction décorée
        """
        users = dict(session).get('profile', None)
        if users:
            return f(*args, **kwargs)
        else:
            return render_template("connectes-toi.html")

    return decorated_function