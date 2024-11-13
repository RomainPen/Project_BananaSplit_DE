import asyncio
import logging
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# URL du proxy
SBR_WS_CDP = "wss://brd-customer-hl_afb68bf9-zone-scraping_browser_atp_matches_2:xl9eql8mb6r1@brd.superproxy.io:9222"

async def fetch_title_atp(browser):
    """Fonction pour charger la page Intersport et récupérer son titre"""
    url_base = "https://www.intersport.fr/"
    page = await browser.new_page()
    await asyncio.sleep(10)
    await page.goto(url_base)
    title = await page.title()
    print(f"Titre de {url_base}: {title}")
    await page.close()


async def fetch_title_decathlon(browser):
    """Fonction pour charger la page Decathlon et récupérer son titre"""
    url_2 = "https://www.decathlon.fr/"
    page = await browser.new_page()
    await asyncio.sleep(5)
    await page.goto(url_2)
    title = await page.title()
    print(f"Titre de {url_2}: {title}")
    await page.close()


async def main():
    async with async_playwright() as p:
        # Connexion au navigateur via le proxy
        browser = await p.chromium.launch()
        
        # Exécuter les deux fonctions de manière concurrente
        await asyncio.gather(
            fetch_title_atp(browser),
            fetch_title_decathlon(browser)
        )

# Exécute le script avec asyncio
if __name__ == "__main__":
    asyncio.run(main())
