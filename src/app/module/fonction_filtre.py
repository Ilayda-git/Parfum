"""
Filtrage pour l'application Streamlit.

Ce module contient des fonctions qui manipulent un DataFrame de parfums :
    - génération de listes d'options pour des widgets (avec/sans "Tous"),
    - filtrage du DataFrame selon des valeurs choisies,
    - recherche texte sur quelques colonnes.
"""

import pandas as pd

def options(df_: pd.DataFrame, col: str):
    """
    Retourne les options d'une colonne, en ajoutant "Tous" en première position.
    Si la colonne est absente, retourne ["Tous"].

    param df_: DataFrame source.
    type df_: pd.DataFrame
    param col: Nom de la colonne.
    type col: str
    return: Liste des options.
    rtype: list[str]
    """
    if col not in df_.columns:
        return ["Tous"]
    vals = sorted(df_[col].dropna().astype(str).unique().tolist())
    return ["Tous"] + vals


def filter_df(base: pd.DataFrame, filters: dict, q: str = "") -> pd.DataFrame:
    """
    Filtre le DataFrame selon les valeurs dans `filters` et une recherche texte `q`.
    
    :param base: DataFrame source
    :type base: pd.DataFrame
    :param filters: Dictionnaire des filtres {colonne: valeur}
    :type filters: dict
    :param q: Texte de recherche
    :type q: str
    :return: DataFrame filtré
    :rtype: pd.DataFrame
    """
    out = base.copy()
    for col, val in filters.items():
        if val != "Tous" and col in out.columns:
            out = out[out[col].astype(str) == str(val)]
    if q.strip():
        q_ = q.strip().lower()
        cols_search = [c for c in ["Fragrance", "Marque", "Parfumeur", "Ingredients_txt", "Concepts_txt"] if c in out.columns]
        if cols_search:
            mask = False
            for c in cols_search:
                mask = mask | out[c].astype(str).str.lower().str.contains(q_, na=False)
            out = out[mask]
    return out


def opts_no_all(df_: pd.DataFrame, col: str):
    """
    Retourne les options d'une colonne, sans "Tous", en mettant "Inconnu" en premier si présent.
    
    param df_: DataFrame source.
    type df_: pd.DataFrame
    param col: Nom de la colonne.
    type col: str
    return: Liste des options.
    rtype: list[str]
    """
    vals = sorted(df_[col].dropna().astype(str).unique().tolist()) if col in df_.columns else ["Inconnu"]
    if "Inconnu" in vals:
        vals = ["Inconnu"] + [v for v in vals if v != "Inconnu"]
    return vals