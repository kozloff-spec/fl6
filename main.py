# from scraper_details import scrap_categories
# from scraper_details import scrape_items

# takes urls from catalog make request for each one and write everything to db
from scraper_details import scrap_catalog
scrap_catalog.scraping_catalogue()

from scraper_details import converter