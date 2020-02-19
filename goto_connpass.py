import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://connpass.com/dashboard/')
    await page.screenshot({'path': 'scraping-1.png'})
    await page.click('.btn.btn_login.github')
    await page.screenshot({'path': 'scraping-2.png'})
    print(vars(page))
	#await page.type(LOGIN_USER_SELECTOR, LOGIN_USER);
    #await page.type(LOGIN_PASS_SELECTOR, LOGIN_PASS);
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
