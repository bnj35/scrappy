from playwright.async_api import async_playwright

async def scrape_jobs():
    jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com/jobs")  # Remplace par un vrai site
        job_elements = await page.query_selector_all(".job")  # Adaptation nécessaire

        for job in job_elements:
            title = await job.inner_text()
            jobs.append(title)

        await browser.close()
    return jobs
