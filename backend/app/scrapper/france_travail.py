import random
from playwright.sync_api import sync_playwright
import os

# Limite le nombre de pages à scrapper pour chaque site
MAX_PAGES = 10
# Limite le temps d'attente par défaut pour les sélecteurs
DEFAULT_TIMEOUT = 10000  # Increase timeout to 5 seconds to handle slow pages

    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@     FRANCE TRAVAIL       @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_france_travail_links():
    try:
        base_url = "https://candidat.francetravail.fr/offres/emploi/developpeur-web/bordeaux/s29m2v9?page={}"
        all_offers = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    page.wait_for_selector('ul.result-list li.result', timeout=DEFAULT_TIMEOUT)
                    
                    # Récupère les informations des offres
                    offers = page.eval_on_selector_all(
                        'ul.result-list li.result',
                        """
                        items => items.map(item => {
                            const title = item.querySelector('.media-body h2.media-heading .media-heading-title')?.textContent.trim();
                            const company = item.querySelector('.subtext')?.textContent.split('-')[0].trim();
                            const location = item.querySelector('.subtext span')?.textContent.trim();
                            const contract = item.querySelector('.contrat')?.textContent.trim();
                            const date = item.querySelector('.date')?.textContent.trim();
                            let offer_url = item.querySelector('a[href]')?.href;

                            // Convert relative URLs to absolute URLs
                            if (offer_url && !offer_url.startsWith('http')) {
                                offer_url = 'https://candidat.francetravail.fr' + offer_url;
                            }

                            return { title, company, location, contract, date, offer_url };
                        })
                        """
                    )

                    if not offers:
                        break
                    all_offers.extend(offers)
                except Exception as e:
                    print(f"Error while scraping France Travail page {page_number}: {e}")
                    break

            browser.close()
            
        # Check if no offers were found
        if not all_offers:
            return []

        return all_offers
    except Exception as e:
        print(f"Erreur dans scrape_france_travail_links: {e}")
        return []
    
