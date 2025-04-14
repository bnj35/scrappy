import random
from playwright.sync_api import sync_playwright
import os


# Limite le nombre de pages à scrapper pour chaque site
MAX_PAGES = 10
# Limite le temps d'attente par défaut pour les sélecteurs
DEFAULT_TIMEOUT = 10000  # Increase timeout to 5 seconds to handle slow pages

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@         HELLO WORK       @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_hellowork_links():
    try:
        base_url = "https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Développeur+web&l=Bordeaux&page={}"
        all_offers = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    page.wait_for_selector('ul[aria-label="liste des offres"] li[data-id-storage-target="item"]', timeout=DEFAULT_TIMEOUT)
                    
                    # Récupère les informations des offres
                    offers = page.eval_on_selector_all(
                        'ul[aria-label="liste des offres"] li[data-id-storage-target="item"]',
                        """
                        items => items.map(item => {
                            const title = item.querySelector('a[aria-label]')?.textContent.trim();
                            const company = item.querySelector('.tw-flex .tw-typo-s')?.textContent.trim();
                            const location = item.querySelector('div[data-cy="localisationCard"]')?.textContent.trim();
                            const contract = item.querySelector('div[data-cy="contractCard"]')?.textContent.trim();
                            const duration = item.querySelector('div[data-cy="contractTag"]')?.textContent.trim();
                            const offer_url = item.querySelector('a[aria-label]')?.href;

                            return { title, company, location, contract, duration, offer_url };
                        })
                        """
                    )

                    if not offers:
                        break
                    all_offers.extend(offers)
                except Exception as e:
                    print(f"Erreur lors de la récupération des offres sur la page {page_number}: {e}")
                    break

            browser.close()
            

        # Check if no offers were found
        if not all_offers:
            return []

        return all_offers
    except Exception as e:
        print(f"Erreur dans scrape_hellowork_links: {e}")
        return []