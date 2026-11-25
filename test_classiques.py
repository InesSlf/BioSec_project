"""Tests : lancer avec `pytest` (ou `python -m pytest`)."""

import pytest

from classiques import (
    cesar_chiffrer, cesar_dechiffrer, cesar_force_brute,
    substitution_chiffrer, substitution_dechiffrer,
    valider_message, valider_cle_substitution,
)

CLE_QWERTY = "QWERTYUIOPASDFGHJKLZXCVBNM"


def test_cesar_exemple_du_sujet():
    assert cesar_chiffrer("BONJOUR", 3) == "ERQMRXU"


def test_cesar_dechiffrer():
    assert cesar_dechiffrer("ERQMRXU", 3) == "BONJOUR"


@pytest.mark.parametrize("k", range(0, 30))
def test_cesar_aller_retour(k):
    assert cesar_dechiffrer(cesar_chiffrer("XYZABC", k), k) == "XYZABC"


def test_force_brute_retourne_25_resultats():
    res = cesar_force_brute("ERQMRXU")
    assert len(res) == 25
    assert [k for k, _ in res] == list(range(1, 26))
    assert (3, "BONJOUR") in res


def test_substitution_exemple_du_sujet():
    assert substitution_chiffrer("ATTAQUE", CLE_QWERTY) == "QZZQJXT"


def test_substitution_dechiffrer():
    assert substitution_dechiffrer("QZZQJXT", CLE_QWERTY) == "ATTAQUE"


def test_substitution_aller_retour_tout_l_alphabet():
    m = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert substitution_dechiffrer(substitution_chiffrer(m, CLE_QWERTY), CLE_QWERTY) == m


@pytest.mark.parametrize("texte", ["", "bonjour", "BON JOUR", "ÉTÉ", "ABC1"])
def test_message_invalide(texte):
    with pytest.raises(ValueError):
        valider_message(texte)


@pytest.mark.parametrize("cle", ["ABC", CLE_QWERTY[:-1] + "Q", CLE_QWERTY.lower(), CLE_QWERTY + "A"])
def test_cle_invalide(cle):
    with pytest.raises(ValueError):
        valider_cle_substitution(cle)


# ------------------------------------------------------------ force brute
from classiques import trouver_cle_cesar

PHRASES = [
    "BONJOUR",
    "NOUSAVONSTROUVELEMESSAGESECRETDANSLEJARDIN",
    "LAREUNIONESTPREVUEDEMAINMATINAVECTOUSLESMEMBRES",
    "ATTAQUEALAUBEPARLECOTEEST",
]


@pytest.mark.parametrize("phrase", PHRASES)
@pytest.mark.parametrize("k", [1, 3, 7, 13, 25])
def test_trouver_cle_cesar(phrase, k):
    cle, texte, _ = trouver_cle_cesar(cesar_chiffrer(phrase, k))
    assert (cle, texte) == (k, phrase)


def test_trouver_cle_avec_couche_suivante():
    # César puis substitution : on retire la substitution avant de noter chaque essai
    phrase = "NOUSAVONSTROUVELEMESSAGESECRETDANSLEJARDIN"
    c = substitution_chiffrer(cesar_chiffrer(phrase, 9), CLE_QWERTY)
    k, texte, _ = trouver_cle_cesar(
        substitution_dechiffrer(c, CLE_QWERTY),
    )
    assert (k, texte) == (9, phrase)


# ------------------------------------------------ transposition, normalisation, challenge
from classiques import normaliser, ACCENTS, SANS_ACCENT
from transposition import chiffrer_transposition, dechiffrer_transposition, ordre_colonnes
from challenge import dechiffrer_couches


def test_transposition_exemple_du_sujet():
    assert chiffrer_transposition("RENDEZVOUSAMIDI", "PORTE") == "ESIEVMRZANOIDUD"
    assert dechiffrer_transposition("ESIEVMRZANOIDUD", "PORTE") == "RENDEZVOUSAMIDI"


def test_transposition_remplissage_et_aller_retour():
    c = chiffrer_transposition("BONJOUR", "PORTE")  # 7 lettres -> complété par des X
    assert len(c) == 10
    assert dechiffrer_transposition(c, "PORTE") == "BONJOURXXX"


def test_transposition_lettres_repetees_dans_le_mot_cle():
    assert ordre_colonnes("BANANE") == [1, 3, 0, 5, 2, 4]
    m = "LEMESSAGEESTLONG"
    assert dechiffrer_transposition(chiffrer_transposition(m, "BANANE"), "BANANE")[:len(m)] == m


def test_transposition_erreurs():
    with pytest.raises(ValueError):
        dechiffrer_transposition("ABCDE", "ABC")  # 5 n'est pas multiple de 3
    with pytest.raises(ValueError):
        chiffrer_transposition("ABC", "")
    with pytest.raises(ValueError):
        chiffrer_transposition("ABC", "pa")


def test_normaliser():
    assert normaliser("Rendez-vous à 18h, café été !") == "RENDEZVOUSAHCAFEETE"
    assert normaliser("Œuvre ÉLÈVE") == "OEUVREELEVE"
    assert len(ACCENTS) == len(SANS_ACCENT)


def test_challenge_trois_couches():
    phrase = "NOUSAVONSTROUVELEMESSAGESECRETDANSLEJARDIN"
    for ordre in ([("cesar", None), ("transposition", "BRUME"), ("substitution", CLE_QWERTY)],
                  [("substitution", CLE_QWERTY), ("cesar", None), ("transposition", "BRUME")],
                  [("transposition", "BRUME"), ("substitution", CLE_QWERTY), ("cesar", None)]):
        c = phrase
        for couche, cle in ordre:
            if couche == "cesar":
                c = cesar_chiffrer(c, 11)
            elif couche == "transposition":
                c = chiffrer_transposition(c, cle)
            else:
                c = substitution_chiffrer(c, cle)
        k, texte, _, etapes = dechiffrer_couches(c, ordre)
        assert k == 11 and texte[:len(phrase)] == phrase and len(etapes) == 3
