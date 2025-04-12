import random
from playwright.sync_api import sync_playwright

# Limite le nombre de pages à scrapper pour chaque site
MAX_PAGES = 2
# Limite le temps d'attente par défaut pour les sélecteurs
DEFAULT_TIMEOUT = 5000  # Increase timeout to 10 seconds to handle slow pages
INDEED_TIMEOUT = 10000  # Increase timeout for Indeed to 10 seconds

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


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@          INDEED          @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_indeed_links():
    try:
        base_url = "https://fr.indeed.com/jobs?q=developpeur+web&l=Bordeaux+%2833%29&radius=25&start=%7B%7D&vjk=dff2ff50493c0214"
        all_offers = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                print(f"Scraping Indeed page: {url}")
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    # Wait for the job list to load
                    page.wait_for_selector('ul.jobsearch-ResultsList', timeout=DEFAULT_TIMEOUT)

                    # Fetch all offers using the new selector structure
                    offers = page.eval_on_selector_all(
                        'li.css-1ac2h1w',  # This is the list item class
                        """
                        items => items.map(item => {
                            const title = item.querySelector('.jobTitle a')?.textContent.trim();
                            const offer_url = item.querySelector('.jobTitle a')?.href;
                            const company = item.querySelector('.company_location .css-1h7lukg')?.textContent.trim();
                            const location = item.querySelector('.company_location .css-1restlb')?.textContent.trim();
                            const contract = item.querySelector('.jobMetaDataGroup')?.textContent.trim() || "Not specified"; // Contract data might be missing

                            return { title, company, location, contract, offer_url };
                        })
                        """
                    )

                    # If no offers found, break the loop
                    if not offers:
                        print("No job offers found on this page.")
                        continue

                    all_offers.extend(offers)

                except Exception as e:
                    print(f"Error while scraping Indeed page {page_number}: {e}")
                    continue

            browser.close()

        # If no offers were found at all
        if not all_offers:
            print("No job offers scraped.")
            return []

        return all_offers
    except Exception as e:
        print(f"Erreur dans scrape_indeed_links: {e}")
        return []


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
                print(f"Scraping France Travail page: {url}")
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

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@     EXECUTION GLOBAL     @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

if __name__ == "__main__":
    offers = scrape_hellowork_links()
    for offer in offers:
        print(f"**Titre**: {offer['title']}")
        print(f"**Entreprise**: {offer['company']}")
        print(f"**Lieu**: {offer['location']}")
        print(f"**Contrat**: {offer['contract']}")
        print(f"**Durée**: {offer['duration']}")
        print(f"**Lien vers l'offre**: {offer['offer_url']}")
        print("-" * 40)

    print("\n#### WELCOME TO THE JUNGLE ####")
    offers = scrape_wttj_links()
    for offer in offers:
        print(f"**Titre**: {offer['title']}")
        print(f"**Entreprise**: {offer['company']}")
        print(f"**Lieu**: {offer['location']}")
        print(f"**Contrat**: {offer['contract']}")
        print(f"**Date de publication**: {offer['date']}")
        print(f"**Lien vers l'offre**: {offer['offer_url']}")
        print("-" * 40)

    print("\n#### INDEED ####")
    offers = scrape_indeed_links()
    for offer in offers:
        print(f"**Titre**: {offer['title']}")
        print(f"**Entreprise**: {offer['company']}")
        print(f"**Lieu**: {offer['location']}")
        print(f"**Salaire**: {offer['salary']}")
        print(f"**Contrat**: {offer['contract']}")
        print(f"**Lien vers l'offre**: {offer['offer_url']}")
        print("-" * 40)

    print("\n#### FRANCE TRAVAIL ####")
    offers = scrape_france_travail_links()
    for offer in offers:
        print(f"**Titre**: {offer['title']}")
        print(f"**Entreprise**: {offer['company']}")
        print(f"**Lieu**: {offer['location']}")
        print(f"**Contrat**: {offer['contract']}")
        print(f"**Date de publication**: {offer['date']}")
        print(f"**Lien vers l'offre**: {offer['offer_url']}")
        print("-" * 40)