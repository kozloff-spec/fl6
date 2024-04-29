import asyncio
import os
from datetime import datetime
# from scraper_details import scrap_categories
from scraper_details import scrape_items
from scraper_details import scrap_catalog
from scraper_details import converter
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def start():
    print('inteval scrapint begin')
    # asyncio.run(scrape_items.scrape_items())
    try:
        # os.remove('db/my_database.db')
        pass
    except :
        pass
    for i in range(1):
        scrap_catalog.scraping_catalogue()
    converter.convert()
    print(datetime.now())



async def main():
    scheduler = AsyncIOScheduler()
    load_dotenv('config')

    scheduler.add_job(start, 'interval', hours=max(1, int(os.getenv('HOW_OFTEN'))))
    scheduler.start()

start()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()