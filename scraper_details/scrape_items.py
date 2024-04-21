import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def scrap_page(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            with open('html.html','w',encoding='utf-8') as f:
                f.write(body)

async def scraper_pages():
    tasks = []
    with open('data/items.txt','r') as f:
        for line in f:
            task = asyncio.create_task(scrap_page(line.strip()))
            tasks.append(task)
            break
        await asyncio.gather(*tasks)

async def scrap(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            soup = BeautifulSoup(body,'html.parser')
            page_counter = soup.find_all('a','j-catalog-pagination-btn')
            pages = page_counter[-2].text.strip() if len(page_counter) >= 2 else 0
            return [url,pages]



async def scraper_items():
    tasks = []
    scraper_tasks = []
    with open('data/categories.txt','r') as f:
        for line in f.readlines():
            task = asyncio.create_task(scrap(line.strip()))
            tasks.append(task)
    for pages in await asyncio.gather(*tasks):
        for page in range(int(pages[1])):
            if int(page) == 0:
                req_for_item = f'{pages[0]}'
            elif page == 1:
                continue
            else:
                req_for_item = f'{pages[0]}filter/page={page}/'
            scraper_tasks.append(req_for_item)
            with open('data/items.txt','w') as f:
                f.write('\n'.join(scraper_tasks))


loop = asyncio.get_event_loop()
# loop.run_until_complete(scraper_items())
loop.run_until_complete(scraper_pages())
