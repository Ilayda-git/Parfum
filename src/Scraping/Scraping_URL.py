"""
Module principal pour le scrapping des URLs des parfums à partir de la page catalogue.
"""

from src.Scraping.module.telechargement_catalogue import recupere_page_complete
from src.Scraping.module.fusion_scrap import serialise
from src.Scraping.module.fonction_scrap_url import extraction_urls
from src.Scraping.module.classe import Catalogue


def main():
    """
    Scrape la page catalogue pour extraire les URLs des parfums et les sauvegarde dans un fichier JSON.
    """
    html = recupere_page_complete()
    parfums = extraction_urls(html)
    resultat = Catalogue(contenu=parfums)
    serialise(resultat=resultat, nom_fichier="parfums_liste_url.json")


if __name__ == "__main__":
    main()
