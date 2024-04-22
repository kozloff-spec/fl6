import requests
from bs4 import BeautifulSoup

def scrape_categories():
    url = 'https://opt-drop.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find('div',class_='productsMenu-tabs-switch').findAll('li')
    categories_list = []
    for category in categories:
        categories_list.append(f"https://opt-drop.com{category.find('a').get('href')}")
    with open('data/categories.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(categories_list))

