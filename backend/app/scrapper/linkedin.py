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
    