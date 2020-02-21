import asyncio
import config
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://connpass.com/dashboard/')
    await page.screenshot({'path': 'images/scraping-1.png'})
    await page.click('.btn.btn_login.github')
    await page.screenshot({'path': 'images/scraping-2.png'})
    content = await page.evaluate('document.body.innerHTML', force_expr=True)
    await page.type('#login_field', config.GITHUB_USERNAME);
    await page.type('#password', config.GITHUB_PASSWORD);
    await page.click("input[name='commit']")
    await page.waitForSelector('.round_box_title');
    await page.screenshot({'path': 'images/scraping-3.png'})
    await page.goto('https://connpass.com/event/164668/stats/',waitUntil='networkidle0')
    await page.screenshot({'path': 'images/scraping-4.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
