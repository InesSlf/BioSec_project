"""César et substitution, écrits à la main (partie Personne A).

Aucune fonction toute faite de chiffrement : seulement ord/chr, des boucles
et de l'arithmétique modulo 26. Conventions : majuscules A-Z, sans espaces.
"""

import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ------------------------------------------------------------ outils de base
def est_majuscule(c: str) -> bool:
    return "A" <= c <= "Z"


def position(c: str) -> int:
    """Rang de la lettre : A=0 ... Z=25."""
    return ord(c) - ord("A")


def lettre(n: int) -> str:
    """Lettre de rang n (modulo 26, y compris pour n négatif)."""
    return chr(n % 26 + ord("A"))


def valider_message(texte: str) -> str:
    if len(texte) == 0:
        raise ValueError("Le message est vide.")
    invalides = []
    for c in texte:
        if not est_majuscule(c) and c not in invalides:
            invalides.append(c)
    if invalides:
        raise ValueError(
            "Seules les lettres majuscules A-Z sont acceptées (ni espaces, ni accents). "
            "Caractères invalides : " + " ".join(repr(c) for c in invalides)
        )
    return texte


def valider_cle_substitution(cle: str) -> str:
    """La clé doit contenir les 26 lettres, chacune une seule fois."""
    if len(cle) != 26:
        raise ValueError(f"La clé doit faire 26 lettres (reçu : {len(cle)}).")
    vue = [False] * 26
    for c in cle:
        if not est_majuscule(c):
            raise ValueError(f"Clé invalide : {c!r} n'est pas une majuscule A-Z.")
        if vue[position(c)]:
            raise ValueError(f"Clé invalide : la lettre {c} apparaît plusieurs fois.")
        vue[position(c)] = True
    return cle


# ------------------------------------------------------------------- César
def cesar_chiffrer(message: str, k: int) -> str:
    """C = (M + k) mod 26"""
    valider_message(message)
    resultat = ""
    for c in message:
        resultat += lettre(position(c) + k)
    return resultat


def cesar_dechiffrer(chiffre: str, k: int) -> str:
    """M = (C - k) mod 26"""
    valider_message(chiffre)
    resultat = ""
    for c in chiffre:
        resultat += lettre(position(c) - k)
    return resultat


def cesar_force_brute(chiffre: str) -> list:
    """Teste les 25 clés : [(1, texte), ..., (25, texte)]."""
    valider_message(chiffre)
    essais = []
    for k in range(1, 26):
        essais.append((k, cesar_dechiffrer(chiffre, k)))
    return essais


# ------------------------------------------------------------ Substitution
def inverser_cle(cle: str) -> str:
    """Clé inverse : si A -> cle[0], alors la lettre cle[0] redonne A."""
    inverse = [""] * 26
    for i in range(26):
        inverse[position(cle[i])] = chr(ord("A") + i)
    return "".join(inverse)


def substitution_chiffrer(message: str, cle: str) -> str:
    valider_message(message)
    valider_cle_substitution(cle)
    resultat = ""
    for c in message:
        resultat += cle[position(c)]
    return resultat


def substitution_dechiffrer(chiffre: str, cle: str) -> str:
    valider_message(chiffre)
    valider_cle_substitution(cle)
    inverse = inverser_cle(cle)
    resultat = ""
    for c in chiffre:
        resultat += inverse[position(c)]
    return resultat


# ------------------------------------------- Force brute : trouver la bonne clé
# Fréquences des lettres en français (en %), de A à Z.
FREQ_FR = [7.64, 0.90, 3.26, 3.67, 14.72, 1.07, 0.87, 0.74, 7.53, 0.61, 0.05, 5.46, 2.97,
           7.10, 5.80, 2.52, 1.36, 6.69, 7.95, 7.24, 6.31, 1.84, 0.04, 0.43, 0.13, 0.33]

# Mots courants cherchés dans le texte (sans espaces, donc comme sous-chaînes).
MOTS_FR = ["BONJOUR", "MESSAGE", "SECRET", "FLAG", "POUR", "DANS", "AVEC", "LES", "DES", "EST",
           "QUE", "QUI", "UNE", "SUR", "PAS", "NOUS", "VOUS", "TOUS", "ETRE", "AVOIR", "MAIS",
           "RENDEZVOUS", "ATTAQUE", "VOICI", "BRAVO", "TROUVE"]


def occurrences(texte: str, mot: str) -> int:
    """Nombre de fois où `mot` apparaît dans `texte` (chevauchements permis)."""
    n = 0
    for i in range(len(texte) - len(mot) + 1):
        if texte[i:i + len(mot)] == mot:
            n += 1
    return n


def score_francais(texte: str) -> float:
    """Plus le score est BAS, plus le texte ressemble à du français.

    Somme de -ln(fréquence de chaque lettre) : une lettre rare (K, W, Y, Z...) coûte
    cher, un E ou un S coûte peu. Chaque mot courant reconnu retire 2 points par lettre.
    """
    score = 0.0
    for c in texte:
        score += -math.log(FREQ_FR[position(c)] / 100)
    for mot in MOTS_FR:
        score -= 2 * len(mot) * occurrences(texte, mot)
    return score


def trouver_cle_cesar(chiffre: str, suite=None):
    """Teste les 25 clés et ne garde que la meilleure.

    `suite` : fonction facultative appliquée à chaque essai avant de le noter
    (utile quand d'autres couches restent à retirer après César).
    Retourne (k, texte, sur) ; `sur` vaut False si le 2e meilleur score est trop proche.
    """
    valider_message(chiffre)
    meilleur_k, meilleur_texte, meilleur_score = 0, "", 0.0
    second_score = 0.0
    for k in range(1, 26):
        texte = cesar_dechiffrer(chiffre, k)
        if suite is not None:
            texte = suite(texte)
        s = score_francais(texte)
        if k == 1 or s < meilleur_score:
            second_score = meilleur_score
            meilleur_k, meilleur_texte, meilleur_score = k, texte, s
        elif k == 2 or s < second_score:
            second_score = s
    return meilleur_k, meilleur_texte, (second_score - meilleur_score) > 3


# ------------------------------------------------ Normalisation (espaces, accents)
ACCENTS = "ÀÂÄÁÃÅàâäáãåÇçÉÈÊËéèêëÎÏÍÌîïíìÔÖÓÒÕôöóòõÙÛÜÚùûüúÑñŸÿ"
SANS_ACCENT = "A" * 12 + "C" * 2 + "E" * 8 + "I" * 8 + "O" * 10 + "U" * 8 + "N" * 2 + "Y" * 2
LIGATURES = [("Œ", "OE"), ("œ", "OE"), ("Æ", "AE"), ("æ", "AE"), ("ß", "SS")]


def normaliser(texte: str) -> str:
    """Rend un texte conforme au sujet : accents retirés, majuscules, et tout ce qui
    n'est pas une lettre (espaces, ponctuation, chiffres) supprimé."""
    resultat = ""
    for c in texte:
        remplacement = None
        for i in range(len(ACCENTS)):
            if ACCENTS[i] == c:
                remplacement = SANS_ACCENT[i]
        for source, cible in LIGATURES:
            if c == source:
                remplacement = cible
        if remplacement is not None:
            resultat += remplacement
        elif "a" <= c <= "z":
            resultat += chr(ord(c) - 32)
        elif est_majuscule(c):
            resultat += c
    return resultat
