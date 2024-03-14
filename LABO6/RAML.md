## Guide de démarrage rapide raml2html

`raml2html` est un outil de génération de documentation HTML à partir de 
fichiers RAML (RESTful API Modeling Language), permettant de transformer 
facilement les spécifications RAML en documents HTML lisibles. Voici 
un guide rapide pour commencer avec `raml2html`, abordant la mise en route, 
les propriétés principales, et quelques exemples d'utilisation.

### Mise en Route

1. **Installation** : `raml2html` nécessite Node.js. Assurez-vous que 
Node.js est installé sur votre système. Vous pouvez installer `raml2html`
via npm (le gestionnaire de paquets de Node.js) en exécutant la commande 
suivante dans votre terminal :

```sh
npm install -g raml2html
```

Cette commande installe `raml2html` globalement, vous permettant de 
l'exécuter depuis n'importe quel dossier dans votre terminal.

2. **Génération de la documentation** : Pour générer un document HTML à partir 
d'un fichier RAML, utilisez la commande suivante :

```sh
raml2html mon_api.raml > mon_api.html
```

Remplacez `mon_api.raml` par le chemin vers votre fichier RAML. 
Cette commande génère un fichier HTML (`mon_api.html`) contenant la 
documentation de votre API.


## Comment documenter son api

Pour documenter efficacement une API avec `raml2html`, il est essentiel de 
comprendre comment structurer votre document RAML avec des détails tels que 
les en-têtes, les routes, les erreurs, et les codes de réponse. Voici comment 
vous pourriez organiser et documenter ces éléments dans votre fichier RAML.

### En-têtes (Headers)

Les en-têtes HTTP dans RAML peuvent être définis globalement ou au niveau de 
chaque méthode. Voici un exemple pour une méthode spécifique :

```yaml
/users:
  get:
    headers:
      Authorization:
        description: Token d'accès nécessaire pour authentifier la requête.
        required: true
        example: Bearer [votreTokenJWT]
```

### Routes (Resources and Methods)

Les ressources (endpoints) et les méthodes (GET, POST, etc.) sont les éléments
fondamentaux de votre API. Voici comment vous pourriez les définir :

```yaml
/users:
  get:
    description: Retourne une liste d'utilisateurs.
    responses:
      200:
        body:
          application/json:
            example: |
              {
                "users": [{"id": 1, "nom": "Doe"}, {"id": 2, "nom": "Smith"}]
              }
  post:
    description: Crée un nouvel utilisateur.
    body:
      application/json:
        example: |
          {
            "nom": "Doe",
            "email": "jdoe@example.com"
          }
    responses:
      201:
        body:
          application/json:
            example: |
              {
                "id": 3,
                "nom": "Doe",
                "email": "jdoe@example.com"
              }
```

### Erreurs et Codes de Réponse

Documenter les réponses potentielles, y compris les erreurs, est crucial pour 
une bonne documentation API. Cela inclut les codes de réponse réussis et 
d'erreur. Voici un exemple incluant des réponses pour des scénarios réussis 
et d'erreur :

```yaml
/users/{userId}:
  get:
    description: Retourne les détails d'un utilisateur spécifique.
    responses:
      200:
        body:
          application/json:
            example: |
              {
                "id": 1,
                "nom": "Doe",
                "email": "jdoe@example.com"
              }
      404:
        body:
          application/json:
            example: |
              {
                "message": "Utilisateur non trouvé"
              }
```

### Documentation des Modèles de Données

Les modèles de données peuvent être utilisés pour réutiliser les structures de 
données dans votre document RAML. Par exemple, vous pouvez définir un modèle 
d'utilisateur pour l'utiliser dans différentes réponses :

```yaml
types:
  User:
    type: object
    properties:
      id: integer
      nom: string
      email: string
    example: |
      {
        "id": 1,
        "nom": "Doe",
        "email": "jdoe@example.com"
      }
```

Et l'utiliser dans une méthode :

```yaml
/users/{userId}:
  get:
    responses:
      200:
        body:
          application/json:
            type: User
```

### Conclusion

En structurant votre document RAML avec des informations claires sur les 
en-têtes, les routes, les réponses (y compris les erreurs), et en documentant 
vos modèles de données, vous créez une base solide pour `raml2html` générer une 
documentation HTML complète et utile pour les consommateurs de votre API.

Pour une documentation plus détaillée et des exemples supplémentaires, 
consultez [le dépôt GitHub officiel de raml2html](https://github.com/raml2html/raml2html).