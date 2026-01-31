"""
Fonctions de scrapping des URLs & de sérialisation des parfums depuis une page HTML.
"""

import re
import json
from pathlib import Path

from .classe import Parfum, Catalogue

BASE_URL = "https://www.wikiparfum.com"


def extraction_urls(page: str) -> list[Parfum]:
    """
    Extrait les URLs des parfums depuis le HTML de la page.
    
    :param page: Contenu HTML de la page
    :type page: str
    :return: Liste des parfums avec nom brut et URL
    :rtype: list[Parfum]
    """
    page_sans_retours = page.replace("\n", " ")
    motif_lien = re.compile(r'<a[^>]+href="(?P<href>/fr/fragrances/[^"]+)"[^>]*>(?P<texte>.*?)</a>') 
    parfums: list[Parfum] = []

    for match in motif_lien.finditer(page_sans_retours): 
        href = match.group("href") 
        texte_html = match.group("texte")
        texte_sans_tags = re.sub(r"<.*?>", " ", texte_html)
        texte_nettoye = re.sub(r"\s+", " ", texte_sans_tags).strip()

        if not texte_nettoye:
            continue
        if texte_nettoye.lower() in {"new", "en savoir plus"}:
            continue

        parfums.append(
            Parfum(
                nom_brut=texte_nettoye,
                url= BASE_URL + href,))
    print(f"{len(parfums)} parfums extraits.")
    return parfums


def serialise(resultat: Catalogue, nom_fichier: str = "parfums_liste_url.json") -> None:
    """
    Sérialise les données dans un fichier JSON.
    
    :param resultat: Données à sérialiser
    :type resultat: Catalogue
    :param nom_fichier: Nom du fichier de sortie
    :type nom_fichier: str
    """
    current_script = Path(__file__).resolve()
    data_dir = current_script.parent.parent.parent / "Data"
    data_dir.mkdir(parents=True, exist_ok=True)
    chemin = data_dir / nom_fichier

    if chemin.exists():
        print(f"Le fichier {chemin} existe déjà, il sera écrasé.")
        chemin.unlink()

    json_str = json.dumps(
        resultat.model_dump(), 
        indent=2, 
        ensure_ascii=False)

    chemin.write_text(json_str, encoding="utf-8")
    print(f"JSON sauvegardé dans {chemin}")
