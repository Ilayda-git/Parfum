"""
Module pour télécharger les pages des fragrances avec Selenium.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def telecharge_page(url: str) -> str:
    """
    Télécharge la page donnée avec Selenium et attend que certains
    éléments soient chargés avant de renvoyer le HTML complet.
    
    :param url: URL de la page à télécharger
    :type url: str
    :return: Contenu HTML de la page
    :rtype: str
    """
    driver = webdriver.Firefox()
    driver.get(url)

    WebDriverWait(driver, 10).until(
        lambda d: "Origine" in d.page_source or "ORIGINE" in d.page_source or "Ingrédients" in d.page_source)

    page = driver.page_source.replace("\n", " ")
    driver.quit()
    return page