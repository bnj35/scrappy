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

def stealth_sync(page):
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
        Object.defineProperty(navigator, 'languages', {get: () => ['fr-FR', 'fr']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
    """)
    
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
                    page.wait_for_selector('#mosaic-jobResults', timeout=DEFAULT_TIMEOUT)

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
    
