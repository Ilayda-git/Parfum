"""
Fonctions pour extraire des données spécifiques depuis le HTML et 
les réponses XHR d'une page de parfum.
"""

import re
import html
import json
from playwright.sync_api import sync_playwright
from src.Scraping.module.telechargment_fragrance import telecharge_page



def extrait_marque(page: str):
    """
    Extrait la marque depuis le HTML de la page.
    
    :param page: Contenu HTML de la page
    :type page: str
    :return: Nom de la marque
    :rtype: str | None
    """
    m = re.search(r'<h6[^>]*>(.*?)</h6>', page)
    if not m:
        return None
    t = re.sub(r"<.*?>", " ", m.group(1))
    return re.sub(r"\s+", " ", t).strip()


def extrait_famille_sous(page: str):
    """
    Extrait la famille et la sous-famille depuis le HTML de la page.
    
    :param page: Contenu HTML de la page
    :type page: str
    :return: Tuple contenant la famille et la sous-famille
    :rtype: tuple[str | None, str | None]
    """
    candidats = re.findall(r'<p[^>]*text-center[^>]*>(.*?)</p>', page)
    
    textes = []
    for c in candidats:
        t = re.sub(r"<.*?>", " ", c)
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            textes.append(t)

    def maj(s):
        """
        Vérifie si une chaîne est en majuscules.
        
        :param s: Chaîne à vérifier
        :type s: str
        returns: booléen indiquant si la chaîne est en majuscules
        :rtype: bool
        """
        lettres = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ]", "", s)
        return lettres != "" and lettres == lettres.upper()

    familles = [t for t in textes if maj(t)]
    famille = familles[0] if len(familles) > 0 else None
    sous_famille = familles[1] if len(familles) > 1 else None
    return famille, sous_famille


def extrait_parfumeur(page: str):
    """
    Extrait le nom du parfumeur depuis le HTML de la page.  
    
    :param page: Contenu HTML de la page
    :type page: str
    returns: Nom du parfumeur
    :rtype: str | None
    """
    m = re.search(r'<dd[^>]*aria-label="([^"]+)"', page)
    return m.group(1) if m else None


def extrait_ingredients(page: str):
    """
    Extrait la liste des ingrédients depuis le HTML de la page.
    
    :param page:  Contenu HTML de la page
    :type page: str
    returns: Liste des ingrédients
    :rtype: list[str]
    """
    m = re.search(
        r'<div class="flex invisible gap-2 flex-wrap mb-6">(.*?)</div>',
        page,
    )
    if not m:
        return []
    bloc = m.group(1)
    items = re.findall(r'>([^<>]+)</(?:a|span)>', bloc)
    return [html.unescape(i.strip()) for i in items if i.strip()]


def extrait_prix(page: str) -> str | None:
    """
    Extrait la catégorie de prix depuis le HTML de la page.
    
    :param page: Contenu HTML de la page
    :type page: str
    :return: Catégorie de prix ("Niche", "Prestige", "Mass Market") ou None si non trouvée
    :rtype: str | None
    """
    page = page.replace("\n", " ")
    dollars_noirs = re.findall(r'<span[^>]*class="[^"]*text-black[^"]*"[^>]*>\$</span>',page)
    count = len(dollars_noirs)
    if count == 3:
        return "Niche"
    elif count == 2:
        return "Prestige"
    elif count == 1:
        return "Mass Market"
    else:
        return None
    
    
def Scrappe_html(url_test):
    """
    Scrappe les données visibles (HTML) d'une page de parfum donnée.
    
    :param url_test: URL de la page du parfum à scraper
    :type url_test: str
    :return: Dictionnaire contenant les données extraites du HTML
    :rtype: dict
    """
    page = telecharge_page(url_test)
    data_html = {
        "Marque": extrait_marque(page),
        "Famille": None,
        "Sous_famille": None,
        "Parfumeur": extrait_parfumeur(page),
        "Ingredients": extrait_ingredients(page),
        "Prix_Categorie": extrait_prix(page)
    }
    fam, sous_fam = extrait_famille_sous(page)
    data_html["Famille"] = fam
    data_html["Sous_famille"] = sous_fam

    return data_html


def Scrappe_xhr(url):
    """
    Scrappe les données techniques (XHR) d'une page de parfum donnée.
    
    :param url: URL de la page du parfum à scraper
    :type url: str
    :return: Dictionnaire contenant les données extraites du XHR
    :rtype: dict | None
    """
    captured_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_response(response):
            try:
                data = response.json()
                if data.get("name") == "DetailDatasheetItems":
                    captured_data.append(data)
            except:
                pass

        page.on("response", handle_response)
        page.goto(url, wait_until="load")
        
        try:
            fragrance_name = page.locator("h1").inner_text()
        except:
            fragrance_name = url.split("/")[-1]

        try:
            fiche_btn = page.locator("text=Fiche technique")
            fiche_btn.wait_for(state="visible", timeout=5000)
            fiche_btn.click()
        except:
            pass

        page.wait_for_timeout(5000)
        browser.close()

    if not captured_data:
        return None

    data_xhr = {"Fragrance": fragrance_name}
    for item in captured_data[0]["props"]["items"]:
        title = item["props"].get("title")
        value = item["props"].get("value")
        if isinstance(value, list):
            value = ", ".join(value)
        data_xhr[title] = value

    return data_xhr