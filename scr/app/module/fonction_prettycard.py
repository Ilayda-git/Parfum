"""
Rendu des cartes parfums dans Streamlit.

Ce module regroupe la logique d'affichage (UI) des résultats sous forme de cartes
stylées, à partir d'un DataFrame de parfums.
"""

import streamlit as st
import pandas as pd
from streamlit_extras.stylable_container import stylable_container


def pretty_cards(df_show: pd.DataFrame, max_cards: int = 30):
    """
    Affiche une liste de cartes (une par parfum) pour les lignes du DataFrame.

    :param df_show: DataFrame des parfums à afficher
    :type df_show: pd.DataFrame
    :param max_cards: Nombre maximum de cartes à afficher
    :type max_cards: int
    """

    for i, r in df_show.head(max_cards).iterrows():
        with stylable_container(
            key=f"carte_parfum_{i}",
            css_styles="""
                {
                    background-color: #fff8f5 ;
                    border: 1px solid #e6d2c4;
                    border-radius: 15px;
                    padding: 20px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
                    margin-bottom: 10px;
                }
                
            """
        ):
            st.markdown(f"### {r.get('Fragrance','')} <span style='font-size:0.8em; color:#888; font-weight:normal'>— {r.get('Marque','')} ({r.get('Année','')})</span>", unsafe_allow_html=True)
            ing = str(r.get("Ingredients_txt", ""))[:120]
            con = str(r.get("Concepts_txt", ""))[:120]
            price = r.get('Prix_Categorie','')
            color_price = "#d35400" if price == "Niche" else "#27ae60"
            
            cF, cSF, cG, cI = st.columns([2, 2, 2, 5])
            with cF: st.markdown(f"**Famille :** {r.get('Famille','')}")
            with cSF: st.markdown(f"**Sous-famille :** {r.get('Sous_famille','')}")
            with cG: st.markdown(f"**Genre :** {r.get('Genre','')}")
            with cI: st.markdown(f"**Ingrédients :** {ing}...")

            cP, cO, cPG, cC = st.columns([2, 2, 2, 5])
            with cP: st.markdown(f"**Parfumeur :** {r.get('Parfumeur','')}")
            with cO: st.markdown(f"**Origine :** {r.get('Origine','')}")
            with cPG: st.markdown(f"**Prix :** <span style='color:{color_price}; font-weight:bold'>{price}</span>", unsafe_allow_html=True)
            with cC: st.markdown(f"**Concepts :** {con}{'…' if len(str(r.get('Concepts_txt',''))) > 120 else ''}")