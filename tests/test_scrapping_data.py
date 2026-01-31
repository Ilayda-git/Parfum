"""
        Tests unitaires / intégration légère pour Scrapping_Data.py
        Objectif : Tester uniquement les fonctions d'extraction "pures" (regex) + fusion

        On fait 2 types de tests :
        1) Tests unitaires sur HTML artificiel (stable)
        2) Test léger sur une vraie page WikiParfum (peut changer selon le site)
"""

import requests
from pathlib import Path
from scr.Scrapping.module import fonction_scrap_data
from scr.Scrapping.module import fusion_scrap

URL_TEST = "https://www.wikiparfum.com/fr/fragrances/ck-one-essence-viva-love"


def find_unique_file(root: Path, filename: str) -> Path:
    """
    Trouve un fichier unique dans un répertoire et ses sous-répertoires.
    
    :param root: Répertoire racine où chercher
    :type root: Path
    :param filename: Nom du fichier à trouver
    :type filename: str
    :return: Chemin vers le fichier unique trouvé
    :rtype: Path
    """
    matches = sorted(root.rglob(filename))
    if not matches:
        raise FileNotFoundError(f"{filename} introuvable sous {root}")
    if len(matches) > 1:
        msg = "\n".join(str(m) for m in matches)
        raise RuntimeError(f"Plusieurs {filename} trouvés, précise le bon :\n{msg}")
    return matches[0]


def fetch_html(url: str) -> str:
    """
    Récupère le HTML d'une page web sans utiliser Selenium.
    
    :param url: URL de la page à récupérer
    :type url: str
    :return: Contenu HTML de la page
    :rtype: str
    """
    r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text


def test_extrait_marque_depuis_html_artificiel():
    """
    Teste l'extraction de la marque depuis du HTML artificiel.
    """
    html = "<h6>Calvin Klein</h6>"
    assert fonction_scrap_data.extrait_marque(html) == "Calvin Klein"


def test_extrait_famille_sous_depuis_html_artificiel():
    """
    Teste l'extraction de la famille et de la sous-famille depuis du HTML artificiel.
    """
    html = """
    <p class="text-center">FLORAL</p>
    <p class="text-center">CITRUS</p>
    """
    fam, sous = fonction_scrap_data.extrait_famille_sous(html)
    assert fam == "FLORAL"
    assert sous == "CITRUS"


def test_extrait_parfumeur_depuis_html_artificiel():
    """
    Teste l'extraction du parfumeur depuis du HTML artificiel.
    """
    html = '<dd aria-label="Alberto Morillas"></dd>'
    assert fonction_scrap_data.extrait_parfumeur(html) == "Alberto Morillas"


def test_extrait_ingredients_depuis_html_artificiel():
    """
    Teste l'extraction des ingrédients depuis du HTML artificiel.
    """
    html = '<div class="flex invisible gap-2 flex-wrap mb-6"><a>bergamote</a><span>citron</span><a>musc</a></div>'
    ingredients = fonction_scrap_data.extrait_ingredients(html)
    assert ingredients == ["bergamote", "citron", "musc"]


def test_extrait_prix_mapping():
    """
    Teste la fonction d'extraction du niveau de prix depuis du HTML artificiel.
    """
    html1 = '<span class="text-black">$</span>'
    html2 = '<span class="text-black">$</span><span class="text-black">$</span>'
    html3 = '<span class="text-black">$</span><span class="text-black">$</span><span class="text-black">$</span>'

    assert fonction_scrap_data.extrait_prix(html1) == "Mass Market"
    assert fonction_scrap_data.extrait_prix(html2) == "Prestige"
    assert fonction_scrap_data.extrait_prix(html3) == "Niche"


def test_fusionne_donnees_priorite_xhr():
    """
    Teste que la fusion des données privilégie les données XHR en cas de conflit.
    """
    d_html = {"Marque": "A", "X": "html"}
    d_xhr = {"Fragrance": "F", "X": "xhr"} 
    out = fusion_scrap.fusionne_donnees(d_html, d_xhr)
    assert out["Marque"] == "A"
    assert out["Fragrance"] == "F"
    assert out["X"] == "xhr"


def test_extractions_depuis_page_reelle_sans_selenium():
    """
    Test léger sur une vraie page (sans Selenium) :
    - On vérifie juste que certaines fonctions renvoient un type cohérent.
    """
    html = fetch_html(URL_TEST)

    marque = fonction_scrap_data.extrait_marque(html)
    famille, sous = fonction_scrap_data.extrait_famille_sous(html)
    prix = fonction_scrap_data.extrait_prix(html)

    assert marque is None or isinstance(marque, str)
    assert famille is None or isinstance(famille, str)
    assert sous is None or isinstance(sous, str)
    assert prix is None or prix in {"Mass Market", "Prestige", "Niche"}