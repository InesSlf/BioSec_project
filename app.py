"""CRYPTA — poste de chiffrement (Streamlit).  streamlit run app.py"""

import math

import streamlit as st

from classiques import (
    ALPHABET, lettre, position, valider_cle_substitution,
    cesar_chiffrer, cesar_dechiffrer, trouver_cle_cesar,
    substitution_chiffrer, substitution_dechiffrer, normaliser,
)
from transposition import chiffrer_transposition, dechiffrer_transposition, ordre_colonnes, completer
from challenge import dechiffrer_couches, NOMS

st.set_page_config(page_title="CRYPTA", page_icon="📟", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=IBM+Plex+Mono:wght@400;600&display=swap');
:root { --amb:#FFB000; --papier:#EFE6C8; --bake:#12110D; --olive:#1C1B14; --ligne:#3b3a2c; }
.stApp { background: repeating-linear-gradient(0deg, #ffffff06 0 1px, transparent 1px 4px),
         radial-gradient(ellipse at 50% 0%, #2a2819 0%, var(--bake) 65%); }
html, body, [class*="st-"], textarea, input { font-family: 'IBM Plex Mono', monospace !important; }
.entete { display:flex; align-items:center; justify-content:center; gap:1.5rem; padding:.5rem 0 0; }
.entete h1 { font-family:'Special Elite', serif !important; font-size:3.6rem; letter-spacing:.18em; color:var(--papier);
  margin:0; text-shadow:0 0 18px #ffb00055; }
.cachet { font-family:'Special Elite', serif; color:#d9483b; border:3px double #d9483b; padding:.2rem .7rem;
  transform:rotate(-8deg); letter-spacing:.2em; font-size:.85rem; opacity:.85; animation:tampon .5s .3s both; }
@keyframes tampon { from { transform:rotate(-8deg) scale(2.2); opacity:0; } }
.sous { text-align:center; color:#8d8668; font-size:.7rem; letter-spacing:.35em; margin:.2rem 0 1.2rem; }
button[data-baseweb="tab"] { font-family:'Special Elite',serif !important; font-size:1.1rem; letter-spacing:.12em; }
.stTextArea textarea, .stTextInput input { background:#0b0a07 !important; border:1px solid var(--ligne) !important;
  border-left:4px solid var(--amb) !important; color:var(--amb) !important; letter-spacing:.3em; text-transform:uppercase;
  border-radius:2px !important; }
.stButton > button { background:var(--olive); color:var(--papier); border:1px solid var(--ligne); border-bottom:4px solid #000;
  border-radius:6px; letter-spacing:.2em; text-transform:uppercase; transition:all .1s; }
.stButton > button:hover { color:var(--amb); border-color:var(--amb); }
.stButton > button:active { border-bottom-width:1px; transform:translateY(3px); }
.telegramme { background:#EFE6C8; color:#1a1710; padding:1rem 1.2rem 1.2rem; margin:1.4rem 0 .6rem; position:relative;
  box-shadow:4px 4px 0 #000; clip-path:polygon(0 0,100% 0,100% calc(100% - 8px),97% 100%,94% calc(100% - 8px),91% 100%,
  88% calc(100% - 8px),85% 100%,82% calc(100% - 8px),79% 100%,76% calc(100% - 8px),73% 100%,70% calc(100% - 8px),67% 100%,
  64% calc(100% - 8px),61% 100%,58% calc(100% - 8px),55% 100%,52% calc(100% - 8px),49% 100%,46% calc(100% - 8px),43% 100%,
  40% calc(100% - 8px),37% 100%,34% calc(100% - 8px),31% 100%,28% calc(100% - 8px),25% 100%,22% calc(100% - 8px),19% 100%,
  16% calc(100% - 8px),13% 100%,10% calc(100% - 8px),7% 100%,4% calc(100% - 8px),0 100%); }
.telegramme .titre { font-family:'Special Elite',serif; font-size:.75rem; letter-spacing:.35em; color:#8a2b22;
  border-bottom:1px dashed #1a171055; padding-bottom:.3rem; margin-bottom:.6rem; }
.telegramme .txt { font-family:'Special Elite',serif; font-size:1.7rem; letter-spacing:.12em; word-break:break-all; }
.telegramme .sp { display:inline-block; width:1.1rem; }
.ch { display:inline-block; animation:frappe .35s both; animation-delay:var(--d); }
@keyframes frappe { 0% { opacity:0; transform:translateY(-10px) scale(1.5); color:#d9483b; } 100% { opacity:1; } }
.lampes { display:flex; flex-direction:column; align-items:center; gap:.4rem; margin:.8rem 0 1rem; }
.lampes div { display:flex; gap:.4rem; }
.lampe { width:2.3rem; height:2.3rem; border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-size:.85rem; color:#4d4b38; background:#0a0906; border:2px solid var(--ligne); box-shadow:inset 0 0 6px #000; }
.lampe.on { animation:allume .4s forwards; animation-delay:var(--d); }
@keyframes allume { to { color:#2a1800; background:var(--amb); border-color:#ffd36b; box-shadow:0 0 14px var(--amb), 0 0 34px #ff8c0066; } }
.legende { text-align:center; color:#8d8668; font-size:.7rem; letter-spacing:.2em; }
.roue-int { transform-origin:160px 160px; animation:tourne 1.1s cubic-bezier(.2,.8,.2,1); }
@keyframes tourne { from { transform:rotate(0deg); } }
.grille { border-collapse:collapse; margin:.6rem auto 1rem; }
.grille td { width:2.3rem; height:2.1rem; text-align:center; border:1px solid var(--ligne); color:var(--papier); }
.grille .cle { background:var(--amb); color:#2a1800; font-weight:600; }
.grille .num { color:var(--amb); font-size:.8rem; border:none; }
</style>
<div class="entete"><h1>CRYPTA</h1><div class="cachet">CONFIDENTIEL</div></div>
<div class="sous">POSTE DE CHIFFREMENT · SÉRIE A</div>
""", unsafe_allow_html=True)


def roue_cesar(k: int) -> str:
    """Disque de César : le disque intérieur tourne de k crans."""
    c, f = 160, []
    f.append(f'<circle cx="{c}" cy="{c}" r="152" fill="#1C1B14" stroke="#3b3a2c" stroke-width="2"/>')
    f.append(f'<circle cx="{c}" cy="{c}" r="112" fill="#12110D" stroke="#FFB000" stroke-width="1"/>')

    def lettres(r, texte_de, col):
        out = []
        for i in range(26):
            deg = -90 + i * 360 / 26
            x, y = c + r * math.cos(math.radians(deg)), c + r * math.sin(math.radians(deg))
            out.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{col}" font-size="14" text-anchor="middle" '
                       f'dominant-baseline="central" transform="rotate({deg + 90:.1f} {x:.1f} {y:.1f})">{texte_de(i)}</text>')
        return "".join(out)

    f.append(lettres(132, lambda i: ALPHABET[i], "#EFE6C8"))
    f.append(f'<g class="roue-int" style="transform:rotate({-k * 360 / 26:.2f}deg)">'
             + lettres(92, lambda i: ALPHABET[i], "#FFB000") + "</g>")
    f.append(f'<circle cx="{c}" cy="{c}" r="52" fill="#0b0a07" stroke="#3b3a2c"/>')
    f.append(f'<text x="{c}" y="{c}" fill="#FFB000" font-size="28" text-anchor="middle" dominant-baseline="central" '
             f'font-family="Special Elite, serif">k={k}</text>')
    f.append('<polygon points="154,0 166,0 160,14" fill="#d9483b"/>')
    return f'<div style="text-align:center"><svg viewBox="0 0 320 320" width="310">{"".join(f)}</svg></div>'


def fils(cle: str) -> str:
    """Tableau de connexions : chaque lettre claire est reliée à sa lettre chiffrée."""
    x = lambda i: 12 + i * 19.6
    parts = []
    for i in range(26):
        parts.append(f'<line x1="{x(i):.1f}" y1="30" x2="{x(position(cle[i])):.1f}" y2="112" stroke="#FFB000" '
                     f'stroke-width="1.3" opacity=".6"/>')
        for y, t in ((16, ALPHABET[i]), (130, ALPHABET[i])):
            parts.append(f'<text x="{x(i):.1f}" y="{y}" fill="#EFE6C8" font-size="11" text-anchor="middle">{t}</text>')
        for y in (26, 116):
            parts.append(f'<circle cx="{x(i):.1f}" cy="{y - 0}" r="2.5" fill="#FFB000"/>')
    return (f'<svg viewBox="0 0 520 140" width="100%">{"".join(parts)}</svg>'
            '<div class="legende">CLAIR (haut) → CHIFFRÉ (bas)</div>')


def lampes(texte: str) -> str:
    """Tableau de lampes AZERTY : les lettres du résultat s'allument dans l'ordre."""
    ordre = []
    for c in texte:
        if c not in ordre:
            ordre.append(c)
    rangs = []
    for ligne in ("AZERTYUIOP", "QSDFGHJKLM", "WXCVBN"):
        cases = ""
        for c in ligne:
            if c in ordre:
                cases += f'<div class="lampe on" style="--d:{min(ordre.index(c) * .12, 3):.2f}s">{c}</div>'
            else:
                cases += f'<div class="lampe">{c}</div>'
        rangs.append(f"<div>{cases}</div>")
    return f'<div class="lampes">{"".join(rangs)}</div>'


def telegramme(titre: str, texte: str, groupes: bool = True, tableau=None):
    tableau = groupes if tableau is None else tableau
    html = ""
    for i, c in enumerate(texte):
        if groupes and i > 0 and i % 5 == 0:
            html += '<span class="sp"></span>'
        html += f'<span class="ch" style="--d:{min(i * .05, 2.5):.2f}s">{c}</span>'
    st.markdown(f'<div class="telegramme"><div class="titre">{titre}</div><div class="txt">{html}</div></div>',
                unsafe_allow_html=True)
    if tableau:
        st.markdown(lampes(texte), unsafe_allow_html=True)
        st.code(texte, language=None)


def executer(fn, titre, *args):
    try:
        resultat = fn(*args)
    except ValueError as e:
        st.error(str(e))
        return
    telegramme(titre, resultat)


def champ(label, key, placeholder, ligne=False):
    """Saisie normalisée : espaces, accents et ponctuation sont retirés automatiquement."""
    brut = st.text_input(label, key=key, placeholder=placeholder) if ligne \
        else st.text_area(label, key=key, placeholder=placeholder)
    propre = normaliser(brut)
    if brut.strip() and propre != brut.strip():
        st.caption(f"Texte utilisé : {propre}")
    return propre


def grille(clair: str, mot_cle: str) -> str:
    """Grille de transposition : mot-clé, numéros d'ordre alphabétique, lignes du message."""
    n, rang = len(mot_cle), [0] * len(mot_cle)
    for p, i in enumerate(ordre_colonnes(mot_cle)):
        rang[i] = p + 1
    clair = completer(clair, n)
    html = "<tr>" + "".join(f'<td class="num">{r}</td>' for r in rang) + "</tr>"
    html += "<tr>" + "".join(f'<td class="cle">{c}</td>' for c in mot_cle) + "</tr>"
    for i in range(0, len(clair), n):
        html += "<tr>" + "".join(f"<td>{c}</td>" for c in clair[i:i + n]) + "</tr>"
    return f'<table class="grille">{html}</table>'


t_cesar, t_subst, t_trans, t_chal = st.tabs(["César", "Substitution", "Transposition", "Challenge"])

with t_cesar:
    mode = st.radio("Opération", ["Chiffrer", "Déchiffrer", "Force brute"], horizontal=True, key="m1")
    texte = champ("Message", "t1", "BONJOUR")
    if mode != "Force brute":
        k = st.slider("Clé k", 0, 25, 3, key="k1")
        st.markdown(roue_cesar(k), unsafe_allow_html=True)
        st.markdown('<div class="legende">EXTÉRIEUR : CLAIR · INTÉRIEUR : CHIFFRÉ</div>', unsafe_allow_html=True)
        if st.button("Transmettre", key="b1"):
            executer(cesar_chiffrer if mode == "Chiffrer" else cesar_dechiffrer, "MESSAGE", texte, k)
    elif st.button("Trouver la clé", key="b2"):
        try:
            k, clair, sur = trouver_cle_cesar(texte)
            telegramme("CLÉ TROUVÉE", f"K = {k}", groupes=False)
            telegramme("TEXTE CLAIR", clair)
            st.markdown('<div class="legende">25 CLÉS TESTÉES · UNE SEULE RETENUE</div>', unsafe_allow_html=True)
            if not sur:
                st.warning("Résultat peu sûr : le message est trop court pour départager les clés.")
        except ValueError as e:
            st.error(str(e))

with t_subst:
    mode_s = st.radio("Opération", ["Chiffrer", "Déchiffrer"], horizontal=True, key="m2")
    texte_s = champ("Message", "t2", "ATTAQUE")
    cle = champ("Clé (26 lettres)", "c2", "QWERTYUIOPASDFGHJKLZXCVBNM", ligne=True)
    try:
        valider_cle_substitution(cle)
        st.markdown(fils(cle), unsafe_allow_html=True)
    except ValueError as e:
        st.caption(f"{len(cle)}/26 — {e}")
    if st.button("Transmettre", key="b3"):
        executer(substitution_chiffrer if mode_s == "Chiffrer" else substitution_dechiffrer, "MESSAGE", texte_s, cle)

with t_trans:
    mode_t = st.radio("Opération", ["Chiffrer", "Déchiffrer"], horizontal=True, key="m3")
    texte_t = champ("Message", "t3", "RENDEZVOUSAMIDI")
    mot = champ("Mot-clé", "c3", "PORTE", ligne=True)
    if st.button("Transmettre", key="b4"):
        try:
            if mode_t == "Chiffrer":
                res = chiffrer_transposition(texte_t, mot)
                clair = texte_t
            else:
                res = dechiffrer_transposition(texte_t, mot)
                clair = res
        except ValueError as e:
            st.error(str(e))
        else:
            st.markdown(grille(clair, mot), unsafe_allow_html=True)
            st.markdown('<div class="legende">CHIFFRÉ = COLONNES LUES DANS L\'ORDRE DES NUMÉROS</div>', unsafe_allow_html=True)
            telegramme("MESSAGE", res)
            if mode_t == "Déchiffrer":
                st.caption("Les X de fin sont le remplissage ajouté au chiffrement.")

with t_chal:
    st.markdown('<div class="legende">MESSAGE À TROIS COUCHES</div>', unsafe_allow_html=True)
    msg = champ("Message intercepté", "t4", "YEXOSOSJCE")
    choix = []
    cols = st.columns(3)
    for i, col in enumerate(cols):
        choix.append(col.selectbox(f"Couche {i + 1}", ["cesar", "transposition", "substitution"],
                                   index=i, key=f"l{i}", format_func=lambda x: NOMS[x]))
    cle_t = champ("Mot-clé de transposition", "c4", "BRUME", ligne=True)
    cle_s = champ("Clé de substitution", "c5", "BADPTGSKFVJYHZXIWCLRNQUOEM", ligne=True)
    if st.button("Déchiffrer le message", key="b5"):
        if len(set(choix)) != 3:
            st.error("Les trois couches doivent être différentes.")
        else:
            couches = [(c, cle_t if c == "transposition" else cle_s if c == "substitution" else None) for c in choix]
            try:
                k, final, sur, etapes = dechiffrer_couches(msg, couches)
            except ValueError as e:
                st.error(str(e))
            else:
                for titre, t in etapes:
                    telegramme(titre, t, tableau=False)
                telegramme("DRAPEAU", "BSD{" + final[:8] + "}", groupes=False)
                if not sur:
                    st.warning("Résultat peu sûr : vérifie que le texte est lisible.")
