import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time



def fetch_title_atp(browser):
    """Fonction pour charger la page Intersport et récupérer son titre"""
    url_base = "https://www.intersport.fr/"
    page = browser.new_page()
    time.sleep(10)
    page.goto(url_base)
    title = page.title()
    print(f"Titre de {url_base}: {title}")
    page.close()


def fetch_title_decathlon(browser):
    """Fonction pour charger la page Decathlon et récupérer son titre"""
    url_2 = "https://www.decathlon.fr/"
    page = browser.new_page()
    time.sleep(10)
    page.goto(url_2)
    title = page.title()
    print(f"Titre de {url_2}: {title}")
    page.close()



def main():
    SBR_WS_CDP = "wss://brd-customer-hl_afb68bf9-zone-scraping_browser_atp_matches_2:xl9eql8mb6r1@brd.superproxy.io:9222"

    with sync_playwright() as p:
        # Connexion au navigateur via le proxy
        browser = p.chromium.launch()
        
        # Exécuter les deux fonctions de manière concurrente
        fetch_title_atp(browser)
        fetch_title_decathlon(browser)





if __name__ == "__main__":
    main()


