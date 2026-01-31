"""
Fonctions avec cache pour le chargement des données et du modèle."""

import streamlit as st
import pandas as pd
import joblib
import re
from pathlib import Path
from collections import Counter

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """
    Charge le dataset des parfums depuis un fichier CSV.

    param path: Chemin du fichier CSV
    type path: Path
    return: DataFrame pandas contenant les données des parfums
    rtype: pd.DataFrame
    """
    try:
        df = pd.read_csv(path, encoding="utf-8")
        # Nettoyage basique
        for col in ["Ingredients_txt", "Concepts_txt"]:
            if col in df.columns:
                df[col] = df[col].fillna("")
        for col in ["Marque", "Famille", "Sous_famille", "Parfumeur", "Origine", "Genre", "Fragrance", "Prix_Categorie"]:
            if col in df.columns:
                df[col] = df[col].fillna("Inconnu")
        if "Année" in df.columns:
            df["Année"] = df["Année"].fillna(df["Année"].median()).astype(int)
        return df
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}")
        return pd.DataFrame()


@st.cache_resource
def load_model(path: Path):
    """
    Charge le modèle de machine learning sauvegardé (format .pkl).

    param path: Chemin du fichier modèle
    type path: Path
    return: Modèle de machine learning chargé
    rtype: Any
    """
    try:
        return joblib.load(path)
    except Exception as e:
        st.error(f"Modèle introuvable ou erreur : {e}")
        return None


@st.cache_data
def build_term_stats(df_: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Construit un tableau de fréquences de termes pour une colonne texte.
    Le CSV stocke `Ingredients_txt` / `Concepts_txt` comme une chaîne de mots séparés par des espaces.
    On extrait donc des *termes* (tokens) et on calcule :
        - nb de parfums contenant le terme ("Parfums")
        - nb d'occurrences totales ("Occurrences")

    :param df_: DataFrame source
    :param col: Nom de la colonne texte
    :return: DataFrame avec colonnes Terme, Parfums, Occurrences
    """
    if col not in df_.columns or df_.empty:
        return pd.DataFrame(columns=["Terme", "Parfums", "Occurrences"])
    stopwords = {
        "de", "d", "du", "des", "la", "le", "les", "l", "un", "une", "et", "ou",
        "a", "à", "au", "aux", "en", "sur", "dans",
    }
    token_re = re.compile(r"[a-zA-ZÀ-ÖØ-öø-ÿ]+(?:'[a-zA-ZÀ-ÖØ-öø-ÿ]+)?")
    perfumes_counter: Counter[str] = Counter()
    occ_counter: Counter[str] = Counter()

    for txt in df_[col].fillna("").astype(str):
        tokens = [t.lower() for t in token_re.findall(txt)]
        tokens = [t for t in tokens if t and t not in stopwords and len(t) >= 2]
        if not tokens:
            continue
        occ_counter.update(tokens)
        perfumes_counter.update(set(tokens))
    out = (
        pd.DataFrame(
            {
                "Terme": list(occ_counter.keys()),
                "Parfums": [perfumes_counter[t] for t in occ_counter.keys()],
                "Occurrences": [occ_counter[t] for t in occ_counter.keys()],
            }
        )
        .sort_values(["Parfums", "Occurrences", "Terme"], ascending=[False, False, True])
        .reset_index(drop=True)
    )
    return out