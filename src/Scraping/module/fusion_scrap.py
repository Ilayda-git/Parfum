"""
Module pour fusionner les données extraites et les sérialiser en JSON.
"""

import json
from pathlib import Path

from src.Scraping.module.classe import Data_base, Donnée_Parfum


def fusionne_donnees(dict_html, dict_xhr) -> Donnée_Parfum:
    """
    Fusionne les données extraites du HTML et du XHR en un seul dictionnaire.
    
    :param dict_html: Dictionnaire des données extraites du HTML
    :type dict_html: dict
    :param dict_xhr: Dictionnaire des données extraites du XHR
    :type dict_xhr: dict
    :return: Dictionnaire fusionné contenant toutes les données
    :rtype: dict
    """
    if not dict_html:
        dict_html = {}
    if not dict_xhr:
        dict_xhr = {}

    resultat_final = {**dict_html, **dict_xhr} 
    return resultat_final


def serialise(resultat: Data_base, nom_fichier: str = "parfums_data_base.json") -> None:
    """
    Sérialise les données dans un fichier JSON.
    
    :param resultat: Données à sérialiser
    :type resultat: Data_base
    :param nom_fichier: Nom du fichier de sortie
    :type nom_fichier: str
    """
    current_script = Path(__file__).resolve() # 
    data_dir = current_script.parent.parent.parent / "Data" #
    data_dir.mkdir(parents=True, exist_ok=True)
    chemin = data_dir / nom_fichier
    if chemin.exists():
        chemin.unlink()

    json_str = json.dumps(
        resultat.model_dump(), 
        indent=2, 
        ensure_ascii=False)
    chemin.write_text(json_str, encoding="utf-8")