"""Transposition par colonnes (code du binôme, repris et sécurisé).

On écrit le message en lignes sous le mot-clé (dernière ligne complétée par des X),
on numérote les colonnes dans l'ordre alphabétique des lettres du mot-clé,
puis on lit chaque colonne de haut en bas dans cet ordre.
"""

from classiques import valider_message


def valider_mot_cle(mot_cle: str) -> str:
    try:
        return valider_message(mot_cle)
    except ValueError as e:
        raise ValueError("Mot-clé : " + str(e)) from None


def ordre_colonnes(mot_cle: str) -> list:
    """Indices des colonnes dans l'ordre alphabétique du mot-clé (tri par insertion, stable :
    deux lettres identiques gardent leur ordre de gauche à droite)."""
    ordre = []
    for i in range(len(mot_cle)):
        j = len(ordre)
        while j > 0 and mot_cle[ordre[j - 1]] > mot_cle[i]:
            j -= 1
        ordre.insert(j, i)
    return ordre


def completer(texte: str, n: int) -> str:
    while len(texte) % n != 0:
        texte += "X"
    return texte


def chiffrer_transposition(texte: str, mot_cle: str) -> str:
    valider_message(texte)
    valider_mot_cle(mot_cle)
    n = len(mot_cle)
    texte = completer(texte, n)
    lignes = [texte[i:i + n] for i in range(0, len(texte), n)]
    colonnes = [""] * n
    for ligne in lignes:
        for j, c in enumerate(ligne):
            colonnes[j] += c
    return "".join(colonnes[i] for i in ordre_colonnes(mot_cle))


def dechiffrer_transposition(texte: str, mot_cle: str) -> str:
    valider_message(texte)
    valider_mot_cle(mot_cle)
    n = len(mot_cle)
    if len(texte) % n != 0:
        raise ValueError(f"Le texte chiffré doit avoir une longueur multiple de {n} "
                         f"(longueur du mot-clé) ; reçu : {len(texte)} lettres.")
    m = len(texte) // n
    colonnes = [""] * n
    for p, i in enumerate(ordre_colonnes(mot_cle)):
        colonnes[i] = texte[p * m:(p + 1) * m]
    return "".join(colonnes[j][r] for r in range(m) for j in range(n))
