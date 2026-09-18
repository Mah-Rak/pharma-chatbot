"""
Utilitaires de traitement de texte.
Normalisation pour la détection de symptômes.
"""
import re
import unicodedata


def normaliser_texte(texte: str) -> str:
    """
    Normalise un texte :
    - minuscules
    - suppression des accents
    - remplacement des apostrophes/tirets par des espaces
    - suppression des caractères non alphanumériques
    - compression des espaces multiples

    Exemple :
        "J'ai MAL à la tête !" → "j ai mal a la tete"
    """
    if not texte:
        return ""

    # Minuscules
    texte = texte.lower()

    # Supprimer les accents
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")

    # Remplacer apostrophes, tirets, underscores par des espaces
    texte = re.sub(r"[''`\-_]", " ", texte)

    # Garder uniquement lettres, chiffres et espaces
    texte = re.sub(r"[^a-z0-9\s]", " ", texte)

    # Compresser les espaces multiples
    texte = re.sub(r"\s+", " ", texte).strip()

    return texte


def contient_expression(texte_normalise: str, expression: str) -> bool:
    """
    Vérifie si une expression est présente dans le texte normalisé.
    Utilise une recherche par mot entier (word boundary).
    """
    expression_norm = normaliser_texte(expression)
    if not expression_norm:
        return False

    pattern = r"\b" + re.escape(expression_norm) + r"\b"
    return bool(re.search(pattern, texte_normalise))
