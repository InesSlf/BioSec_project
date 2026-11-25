"""Déchiffrement d'un message à trois couches (César + substitution + transposition)."""

from classiques import (
    cesar_dechiffrer, trouver_cle_cesar, substitution_dechiffrer, valider_message,
)
from transposition import dechiffrer_transposition

NOMS = {"cesar": "César", "substitution": "Substitution", "transposition": "Transposition"}


def retirer(couche: str, texte: str, cle) -> str:
    if couche == "substitution":
        return substitution_dechiffrer(texte, cle)
    if couche == "transposition":
        return dechiffrer_transposition(texte, cle)
    raise ValueError(f"Couche inconnue : {couche}")


def retirer_liste(couches: list, texte: str) -> str:
    for couche, cle in couches:
        texte = retirer(couche, texte, cle)
    return texte


def dechiffrer_couches(chiffre: str, couches: list):
    """`couches` : [(type, clé), ...] dans l'ordre du CHIFFREMENT (couche 1 d'abord).

    On retire les couches dans l'ordre inverse. La clé de César est trouvée par force
    brute ; les couches à retirer après César servent à noter chaque essai.
    Retourne (k, texte_final, sûr, étapes) où étapes = [(libellé, texte), ...].
    """
    valider_message(chiffre)
    ordre = couches[::-1]
    i_cesar = None
    for i in range(len(ordre)):
        if ordre[i][0] == "cesar":
            i_cesar = i
    if i_cesar is None:
        raise ValueError("Aucune couche César dans la liste.")
    etapes, texte = [], chiffre
    for couche, cle in ordre[:i_cesar]:
        texte = retirer(couche, texte, cle)
        etapes.append((f"APRÈS {NOMS[couche].upper()}", texte))
    apres = ordre[i_cesar + 1:]
    k, _, sur = trouver_cle_cesar(texte, suite=lambda t: retirer_liste(apres, t))
    texte = cesar_dechiffrer(texte, k)
    etapes.append((f"APRÈS CÉSAR (k = {k})", texte))
    for couche, cle in apres:
        texte = retirer(couche, texte, cle)
        etapes.append((f"APRÈS {NOMS[couche].upper()}", texte))
    return k, texte, sur, etapes
