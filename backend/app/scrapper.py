import random
from playwright.sync_api import sync_playwright

# Limite le nombre de pages à scrapper pour chaque site
MAX_PAGES = 10

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@         HELLO WORK       @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_hellowork_links():
    try:
        base_url = "https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Développeur+web&l=Bordeaux&page={}"
        all_links = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                print(f"Scraping HelloWork page: {url}")
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    page.wait_for_selector("a[class*=job-title]", timeout=5000)
                    links = page.eval_on_selector_all(
                        "a[class*=job-title]",
                        "elements => elements.map(el => el.href)"
                    )
                    if not links:
                        print("No links found on this page.")
                        break
                    all_links.extend(links)
                except Exception as e:
                    print(f"Error while scraping HelloWork page {page_number}: {e}")
                    break

            browser.close()

        return all_links
    except Exception as e:
        print(f"Erreur dans scrape_hellowork_links: {e}")
        return []

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@  WELCOME TO THE JUNGLE   @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_wttj_links():
    try:
        base_url = "https://www.welcometothejungle.com/fr/jobs?query=développeur%20web&page={}&aroundQuery=Bordeaux&aroundLatLng=44.84044%2C-0.5805&aroundRadius=20"
        all_links = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                print(f"Scraping Welcome to the Jungle page: {url}")
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    page.wait_for_selector("a[data-testid='job-card-link']", timeout=5000)
                    links = page.eval_on_selector_all(
                        "a[data-testid='job-card-link']",
                        "els => els.map(e => e.href)"
                    )
                    if not links:
                        print("No links found on this page.")
                        break
                    all_links.extend(links)
                except Exception as e:
                    print(f"Error while scraping WTTJ page {page_number}: {e}")
                    break

            browser.close()
        return all_links
    except Exception as e:
        print(f"Erreur dans scrape_wttj_links: {e}")
        return []

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@          INDEED          @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_indeed_links():
    try:
        base_url = "https://fr.indeed.com/jobs?q=developpeur+web&l=Bordeaux+%2833%29&radius=25&start={}"
        all_links = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            for page_number in range(0, MAX_PAGES):
                url = base_url.format(page_number * 10)
                print(f"Scraping Indeed page: {url}")
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    page.wait_for_selector('#mosaic-jobResults', timeout=5000)
                    links = page.eval_on_selector_all(
                        '#mosaic-jobResults a[data-hide-spinner="true"][href*="/rc/clk"]',
                        "els => els.map(el => el.href)"
                    )
                    if not links:
                        print("No links found on this page.")
                        break
                    all_links.extend(links)
                except Exception as e:
                    print(f"Error while scraping Indeed page {page_number}: {e}")
                    break

            browser.close()
        return all_links
    except Exception as e:
        print(f"Erreur dans scrape_indeed_links: {e}")
        return []

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@     FRANCE TRAVAIL       @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

def scrape_france_travail_links():
    try:
        base_url = "https://candidat.francetravail.fr/offres/emploi/developpeur-web/bordeaux/s29m2v9?page={}"
        all_links = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            for page_number in range(1, MAX_PAGES + 1):
                url = base_url.format(page_number)
                print(f"Scraping France Travail page: {url}")
                page.goto(url)
                page.wait_for_timeout(random.randint(1500, 3000))

                try:
                    page.wait_for_selector("div#results-list li a", timeout=5000)
                    links = page.eval_on_selector_all(
                        "div#results-list li a[href*='/offres/emploi/']",
                        "els => els.map(el => el.href)"
                    )
                    if not links:
                        print("No links found on this page.")
                        break
                    all_links.extend(links)
                except Exception as e:
                    print(f"Error while scraping France Travail page {page_number}: {e}")
                    break

            browser.close()
        return all_links
    except Exception as e:
        print(f"Erreur dans scrape_france_travail_links: {e}")
        return []

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
#@@@@@     EXECUTION GLOBAL     @@@@#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

if __name__ == "__main__":
    print("\n#### HELLOWORK ####")
    for link in scrape_hellowork_links():
        print(link)

    print("\n#### WELCOME TO THE JUNGLE ####")
    for link in scrape_wttj_links():
        print(link)

    print("\n#### INDEED ####")
    for link in scrape_indeed_links():
        print(link)

    print("\n#### FRANCE TRAVAIL ####")
    for link in scrape_france_travail_links():
        print(link)