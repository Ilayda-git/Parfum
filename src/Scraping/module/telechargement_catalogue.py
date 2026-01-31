"""
Module pour récupérer les URLs des parfums depuis la page des fragrances en utilisant Selenium.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


BASE_URL = "https://www.wikiparfum.com"
FRAGRANCES_URL = f"{BASE_URL}/fr/fragrances/"

def recupere_page_complete(url: str = FRAGRANCES_URL) -> str:
    """
    Utilise Selenium pour charger une page web et cliquer sur le bouton "En savoir plus"
    jusqu'à ce que tout le contenu soit chargé ou qu'un maximum de clics soit atteint.
    
    :param url: URL de la page à charger
    :type url: str
    :return: Contenu HTML complet de la page après avoir cliqué sur tous les boutons
    :rtype: str
    """
    driver = webdriver.Firefox()  
    driver.get(url)
    wait = WebDriverWait(driver, 8)

    for i in range(250):
        try:
            print(f"Clic {i+1}/250 sur 'En savoir plus'...")
            bouton = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'En savoir plus')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", bouton)
            time.sleep(1.5)

        except TimeoutException:
            print("Plus de bouton 'En savoir plus' – arrêt des clics.")
            break
        except ElementClickInterceptedException as e:
            print("Clique intercepté, on arrête les clics :", e)
            break

    html_complet = driver.page_source
    driver.quit()
    return html_complet