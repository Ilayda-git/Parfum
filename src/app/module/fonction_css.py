"""
Module pour charger et appliquer un fichier CSS local dans une application Streamlit.
"""

import streamlit as st
from pathlib import Path

def local_css(file_name):
    """
    Charge et applique un fichier CSS local pour personnaliser l'interface Streamlit.

    :param file_name: Nom du fichier CSS
    :type file_name: str
    """
    candidates = [
        Path(__file__).parent / file_name,
        Path(__file__).parent.parent / "style" / file_name,
    ]
    for css_path in candidates:
        if css_path.exists():
            with open(css_path, encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            return
    st.error(f"Fichier CSS introuvable. Chemins testés : {', '.join(str(p) for p in candidates)}")