# CRYPTA — outil de chiffrement classique

Outil Python / Streamlit : César, substitution (et transposition à venir).

## Installation
```bash
pip install -r requirements.txt
```

## Lancer l'interface
```bash
streamlit run app.py
```

## Lancer les tests
```bash
pytest
```

## Structure
- `classiques.py` : algorithmes écrits à la main (ord/chr, boucles, modulo 26), sans dépendance à l'interface
- `app.py` : interface Streamlit (un onglet par chiffre)
- `test_classiques.py` : tests unitaires, dont les exemples du sujet

## Conventions
Majuscules A-Z uniquement, sans espaces ni accents.
- César : `C = (M + k) mod 26`
- Substitution : A → 1re lettre de la clé, B → 2e, etc.
