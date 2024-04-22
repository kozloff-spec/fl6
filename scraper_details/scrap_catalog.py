import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time

import sqlite3

from pprint import pprint




async def scrape(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                soup = BeautifulSoup(await resp.text(),'lxml')
                print(url)
                descript = soup.find('div',class_='product-description')
                if soup.find('div',class_='product-description'):
                    descript2 = [desc.text.strip() for desc in descript.find_all('p') if desc.text.strip() != '']
                else:
                    descript2 = ''
                img_list = soup.find('ul',class_='gallery__photos-list').find_all('img')



                data = {}
                data['url'] = url
                data['name'] = soup.find('h1',class_='product-title').text.strip()
                data['available'] = soup.find('div',class_='order-box__availability').text.strip() == 'В наявності'
                data['price'] = ''.join([letter for letter in soup.find('div',class_='product-price__item').text.strip() if letter in '1234567890.'])
                data['description'] = descript2
                data['img_list'] = ['https://opt-drop.com'+img.get('src') for img in img_list]
                data['category'] = soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[1].text.strip()

                if data['name'] == '': data['name'] = ''
                return data

    except Exception as e:
        print('some error ',url,'error id -',e)
        return 'nothing here'



async def main():


    tasks = []
    id = 0
    with open('data/catalog.txt') as file:

        for row in file.readlines():
            row.strip()
            task = asyncio.create_task(scrape(row.strip()))
            tasks.append(task)
            id+=1
            # print(id)

    data = await asyncio.gather(*tasks)
    connection = sqlite3.connect('db/my_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    url TEXT NOT NULL,
    available BOOLEAN,
    category TEXT,
    description TEXT,
    price TEXT,
    img_one TEXT,
    img_two TEXT,
    img_three TEXT,
    img_four TEXT,
    img_five TEXT,
    img_six TEXT,
    img_seven TEXT,
    img_eight TEXT,
    img_nine TEXT,
    img_ten TEXT
    )
    ''')
    for item in data:
        if item == 'nothing here':
            continue
        # pprint(item)
        # if item['name'] == None or item['name'] == '' or not item['name']:
        try:
            cursor.execute('INSERT INTO products (name, url, available,category,description,price,img_one,img_two,img_three,img_four,img_five,img_six,img_seven,img_eight,img_nine,img_ten) VALUES (?,?, ?, ?, ?, ?, ?, ? ,? ,?, ? ,? ,?, ? ,? ,?)', (
                item['name'],
                item['url'],
                item['available'],
                item['category'],
                ' '.join(item['description']),
                item['price'],
                item['img_list'][0] if len(item['img_list']) > 1 else '',
                item['img_list'][1] if len(item['img_list']) > 2 else '',
                item['img_list'][2] if len(item['img_list']) > 3 else '',
                item['img_list'][3] if len(item['img_list']) > 4 else '',
                item['img_list'][4] if len(item['img_list']) > 5 else '',
                item['img_list'][5] if len(item['img_list']) > 6 else '',
                item['img_list'][6] if len(item['img_list']) > 7 else '',
                item['img_list'][7] if len(item['img_list']) > 8 else '',
                item['img_list'][8] if len(item['img_list']) > 9 else '',
                item['img_list'][9] if len(item['img_list']) > 10 else ''


                ))
        except:
            print(item)
    connection.commit()
    connection.close()


def scraping_catalogue():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(time.time() - start_time)