import random
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from dotenv import load_dotenv
import os

load_dotenv()

# Limite le nombre de pages à scrapper pour chaque site
MAX_PAGES = 10
# Limite le temps d'attente par défaut pour les sélecteurs
DEFAULT_TIMEOUT = 10000  # Increase timeout to 5 seconds to handle slow pages
INDEED_TIMEOUT = 10000  # Increase timeout for Indeed to 10 seconds

def stealth_sync(page):
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
        Object.defineProperty(navigator, 'languages', {get: () => ['fr-FR', 'fr']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
    """)


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
        base_url = "https://fr.indeed.com/jobs?q=developpeur+web&l=Bordeaux+%2833%29&ts=1744443776293&from=searchOnHP&rq=1&rsIdx=0&newcount=65&fromage=last&vjk=36d2ba88ec862be1"
        all_offers = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=100)  # Set headless to False for better debugging
            context = browser.new_context(
                locale="fr-FR",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            
            # Vérifie si la variable d'environnement COOKIE_INDEED est définie
            # indeed_cookie_session = os.getenv("COOKIE_INDEED_SESSION")
            # indeed_cookie_csrf = os.getenv("COOKIE_INDEED_CSRF")
            # indeed_cookie_cf_clearance = os.getenv("COOKIE_INDEED_CF_CLEARANCE")

            # context.add_cookies(
            #     [
            #         {
            #             "name": "JSESSIONID",
            #             "value": indeed_cookie_session,
            #             "domain": ".indeed.com",
            #             "path": "/",
            #             "httpOnly": True,
            #             "secure": True
            #         },
            #         {
            #             "name": "CSRF",
            #             "value": indeed_cookie_csrf,
            #             "domain": ".indeed.com",
            #             "path": "/",
            #             "httpOnly": True,
            #             "secure": True
            #         },
            #         {
            #             "name": "cf_clearance",
            #             "value": indeed_cookie_cf_clearance,
            #             "domain": ".indeed.com",
            #             "path": "/",
            #             "httpOnly": False,  
            #             "secure": True
            #         }
            #     ]
            # )
            page = context.new_page()
            stealth_sync(page)

            # Ouvre une page normale pour initier la session
            page.goto("https://www.indeed.com/jobs", timeout=6000)
            page.wait_for_timeout(3000)

            for page_number in range(MAX_PAGES):
                url = base_url.format(page_number * 25)
                print(f"🔎 Scraping page {page_number + 1}: {url}")
                page.goto(url, timeout=6000)
                page.wait_for_timeout(random.uniform(2000, 4000))

                try:
                    for _ in range(3):
                        page.mouse.wheel(0, 1000)
                        page.wait_for_timeout(random.uniform(1000, 2000))
                        
                        # page_content = page.content()
                        # print(page_content)

                    # Attend que les résultats des offres soient chargés
                    page.wait_for_selector('#mosaic-jobResults', timeout=INDEED_TIMEOUT)

                    # Scraping des offres avec le bon sélecteur
                    offers = page.eval_on_selector_all(
                        'li.css-1ac2h1w.eu4oa1w0',
                        """
                        items => items.map(item => {
                            const title = item.querySelector('.jobTitle a')?.textContent.trim();
                            const offer_url = item.querySelector('.jobTitle a')?.href;
                            const company = item.querySelector('.company_location .css-1h7lukg')?.textContent.trim();
                            const location = item.querySelector('.company_location .css-1restlb')?.textContent.trim();
                            const contract = item.querySelector('.jobMetaDataGroup')?.textContent.trim() || "Non spécifié"; // Parfois absent

                            return { title, company, location, contract, offer_url };
                        })
                        """
                    )

                    if not offers:
                        print("⚠️ Aucune offre détectée.")
                        continue

                    all_offers.extend(offers)

                except Exception as e:
                    print(f"❌ Erreur page {page_number + 1}: {e}")
                    continue

            browser.close()
            

        if not all_offers:
            print("❌ Aucune offre récupérée.")
            return []

        print(f"✅ {len(all_offers)} offres récupérées.")
        return all_offers

    except Exception as e:
        print(f"🔥 Erreur globale: {e}")
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
#@@@@@         LINKEDIN         @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_linkedin_links():
    try:
        base_url = "https://www.linkedin.com/jobs/search/?currentJobId=4169994755&distance=25&geoId=104787182&keywords=developpeur%20web&origin=JOBS_HOME_SEARCH_CARDS"
        all_offers = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=100)
            context = browser.new_context(
                locale="fr-FR",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            
            linkedin_cookie = os.getenv("COOKIE_LINKEDIN")
            if not linkedin_cookie:
                raise ValueError("COOKIE_LINKEDIN environment variable is not set")

            context.add_cookies([{
                "name": "li_at",
                "value": linkedin_cookie,
                "domain": ".linkedin.com",
                "path": "/",
                "httpOnly": True,
                "secure": True
            }])

            page = context.new_page()
            stealth_sync(page)

            # Open a normal page to trigger the session
            page.goto("https://www.linkedin.com/feed/", timeout=60000)
            page.wait_for_timeout(3000)

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                page.goto(url, timeout=60000)
                page.wait_for_timeout(random.uniform(2000, 4000))

                try:
                    for _ in range(3):
                        page.mouse.wheel(0, 1000)
                        page.wait_for_timeout(random.uniform(1000, 2000))

                    # Wait for job cards to load
                    page.wait_for_selector("li[data-occludable-job-id]", timeout=15000)

                    offers = page.eval_on_selector_all(
                        "li[data-occludable-job-id]",
                        """items => items
                          .map(item => {
                              const linkEl = item.querySelector('a.job-card-list__title--link');
                              const companyEl = item.querySelector('span.OCTJiTfuvRoNbAplEIjfcyoefuRMlttDng');
                              const locationEl = item.querySelector('.job-card-container__metadata-wrapper li span');

                              return {
                                  title: linkEl?.getAttribute('aria-label')?.trim() || null,
                                  company: companyEl?.innerText?.trim() || null,
                                  location: locationEl?.innerText?.trim() || null,
                                  offer_url: linkEl?.href?.startsWith('/') ? 'https://www.linkedin.com' + linkEl.href : linkEl?.href || null
                              };
                          })
                          .filter(job => job.title && job.offer_url)"""  # Filter out invalid jobs
                    )

                    if not offers:
                        print("⚠️ No job offers detected.")
                        continue

                    all_offers.extend(offers)

                except Exception as e:
                    print(f"❌ Error on page {page_number + 1}: {e}")
                    continue

            browser.close()

        # Remove duplicates
        unique_offers = {}
        for offer in all_offers:
            if offer['title'] not in unique_offers:
                unique_offers[offer['title']] = offer

        all_offers = list(unique_offers.values())

        if not all_offers:
            print("❌ No job offers retrieved.")
            return []

        print(f"✅ {len(all_offers)} unique job offers retrieved.")
        return all_offers

    except Exception as e:
        print(f"🔥 Global error: {e}")
        return []
    
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@     EXECUTION GLOBAL     @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

if __name__ == "__main__":
    offers = scrape_linkedin_links()
    print('####LinkedIn####')
    print(offers)