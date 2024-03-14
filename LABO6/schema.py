valider_nouvel_utilisateur_schema = {
    "type": "object",
    "properties": {
        "nom": {"type": "string"},
        "prenom": {"type": "string"},
        "age": {"type": "integer"},
        "date_naissance": {"type": "string", "format": "date"},
        "grades_universitaires": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["nom", "prenom", "age", "date_naissance", "grades_universitaires"],
    "additionalProperties": False
}


modifier_utilisateur_schema = {
  "type": "object",
  "properties": {
    "nom": {"type": "string"},
    "prenom": {"type": "string"},
    "age": {"type": "integer"},
    "date_naissance": {"type": "string", "format": "date"},
    "grades_universitaires": {
        "type": "array",
        "items": {"type": "string"}
    }
  },
  "additionalProperties": False
}