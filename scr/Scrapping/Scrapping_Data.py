"""
Module principal pour le scrapping des données de parfums à partir des URLs.
"""

import json
from pathlib import Path
from scr.Scrapping.module.fonction_scrap_data import Scrappe_html, Scrappe_xhr
from scr.Scrapping.module.fusion_scrap import fusionne_donnees, serialise

from scr.Scrapping.module.classe import Data_base


current_script = Path(__file__).resolve()
ROOT = current_script.parents[2]          # Scrap_mode
chemin_json = ROOT / "data" / "parfums_liste_url.json"

with open(chemin_json, "r", encoding="utf-8") as f:
    liste_url = json.load(f)["contenu"]

données_parfums = []


def main():
    """
    Scrape les données de chaque parfum à partir de leurs URLs et les sauvegarde dans un fichier JSON.
    """
    for index, item in enumerate(liste_url):
        print(f"[{index}/{len(liste_url)}] Scraping {item['url']}")
        url = item["url"]
        all = fusionne_donnees(Scrappe_html(url), Scrappe_xhr(url))
        données_parfums.append(all)
        SEr = Data_base(contenu=données_parfums)
        
        serialise(SEr, nom_fichier="parfums_data_base.json")
        
    print("Scraping terminé.")


if __name__ == "__main__":
    main()