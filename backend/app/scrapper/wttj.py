import random
from playwright.sync_api import sync_playwright
import os


# Limite le nombre de pages à scrapper pour chaque site
MAX_PAGES = 10
# Limite le temps d'attente par défaut pour les sélecteurs
DEFAULT_TIMEOUT = 10000  # Increase timeout to 5 seconds to handle slow pages

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@  WELCOME TO THE JUNGLE   @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_wttj_links():
    try:
        base_url = "https://www.welcometothejungle.com/fr/jobs?query=d%C3%A9veloppeur%20web&page=1&aroundQuery=Bordeaux&aroundLatLng=44.84044%2C-0.5805&aroundRadius=20&refinementList%5Boffices.country_code%5D%5B%5D=FR"
        all_offers = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    page.wait_for_selector('ul[data-testid="search-results"] li[data-testid="search-results-list-item-wrapper"]', timeout=DEFAULT_TIMEOUT)

                    offers = page.eval_on_selector_all(
                        'ul[data-testid="search-results"] li[data-testid="search-results-list-item-wrapper"]',
                        """
                        items => items.map(item => {
                            const title = item.querySelector('h4.sc-lizKOf')?.textContent.trim();
                            const company = item.querySelector('span.sc-lizKOf.LGoxu')?.textContent.trim();
                            const location = item.querySelector('p.sc-lizKOf.bHifMy .sc-dnvZjJ')?.textContent.trim();
                            const contract = item.querySelector('.sc-bXCLTC .sc-kbdlSk')?.textContent.trim();
                            const date = item.querySelector('time span')?.textContent.trim();
                            const offer_url = item.querySelector('a')?.href;

                            return { title, company, location, contract, date, offer_url };
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
            

        if not all_offers:
            return []

        return all_offers
    except Exception as e:
        print(f"Erreur dans scrape_wttj_links: {e}")
        return []