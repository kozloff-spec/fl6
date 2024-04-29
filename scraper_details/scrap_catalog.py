import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

import sqlite3

from pprint import pprint




async def scrape(url):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_ctx)) as session:
            data = {}
            cookies = {
                'sbjs_migrations': '1418474375998%3D1',
                'sbjs_first_add': 'fd%3D2024-04-21%2020%3A36%3A48%7C%7C%7Cep%3Dhttps%3A%2F%2Fopt-drop.com%2F%7C%7C%7Crf%3D%28none%29',
                'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
                '_ga': 'GA1.1.1403131737.1713721009',
                'sbjs_current': 'typ%3Dreferral%7C%7C%7Csrc%3Dfreelancehunt.com%7C%7C%7Cmdm%3Dreferral%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%2F%7C%7C%7Ctrm%3D%28none%29',
                'uuid': 'f3af9a0fa0c548fe42097c148f24edfa',
                'sbjs_current_add': 'fd%3D2024-04-26%2010%3A45%3A28%7C%7C%7Cep%3Dhttps%3A%2F%2Fopt-drop.com%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Ffreelancehunt.com%2F',
                'sbjs_udata': 'vst%3D31%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F124.0.0.0%20Safari%2F537.36',
                '_gcl_au': '1.1.1941513108.1713934774.653235250.1714302470.1714303552',
                'PHPSESSID': '6bn9v0i4au2abd5bk8rfej0dmg',
                'sbjs_session': 'pgs%3D26%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fopt-drop.com%2Fperenosnyi-likhtar-iz-soniachnoiu-panelliu-ta-poverbankom-25vt-1500mah-gl-2289-ruchnyi-led-svitylnyk%2F',
                '_ga_GMVE0BZ52P': 'GS1.1.1714302465.34.1.1714303719.60.0.436943450',
            }

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,cy;q=0.6,tr;q=0.5,es;q=0.4',
                'cache-control': 'no-cache',
                # 'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_first_add=fd%3D2024-04-21%2020%3A36%3A48%7C%7C%7Cep%3Dhttps%3A%2F%2Fopt-drop.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; _ga=GA1.1.1403131737.1713721009; sbjs_current=typ%3Dreferral%7C%7C%7Csrc%3Dfreelancehunt.com%7C%7C%7Cmdm%3Dreferral%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%2F%7C%7C%7Ctrm%3D%28none%29; uuid=f3af9a0fa0c548fe42097c148f24edfa; sbjs_current_add=fd%3D2024-04-26%2010%3A45%3A28%7C%7C%7Cep%3Dhttps%3A%2F%2Fopt-drop.com%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Ffreelancehunt.com%2F; sbjs_udata=vst%3D31%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F124.0.0.0%20Safari%2F537.36; _gcl_au=1.1.1941513108.1713934774.653235250.1714302470.1714302569; PHPSESSID=ufncei8vg1350at6cdds9175rf; sbjs_session=pgs%3D12%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fopt-drop.com%2Fperenosnyi-likhtar-iz-soniachnoiu-panelliu-ta-poverbankom-25vt-1500mah-gl-2289-ruchnyi-led-svitylnyk%2F; _ga_GMVE0BZ52P=GS1.1.1714302465.34.1.1714302570.41.0.436943450',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'referer': 'https://opt-drop.com/perenosnyi-likhtar-iz-soniachnoiu-panelliu-ta-poverbankom-25vt-1500mah-gl-2289-ruchnyi-led-svitylnyk/',
                'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            }
            async with session.get(url,cookies=cookies,headers=headers) as resp:
                soup = BeautifulSoup(await resp.text(),'lxml')
                print(url,' - ',resp.status)
                descript = soup.find('div',class_='product-description').findChildren() if soup.find('div',class_='product-description') else ' '
                # if soup.find('div',class_='product-description'):
                #     descript2 = [desc.text.strip() for desc in descript.find_all('p') if desc.text.strip() != '']
                # else:
                #     descript2 = ''
                # print(str(descript[0]))
                # print(type(descript[0]))
                # print(''.join([child for child in descript if child != '\n']))
                # descript =  [child for child in descript if child != '\n']
                img_list = soup.find('ul',class_='gallery__photos-list').find_all('img')





                data['url'] = url
                data['name'] = soup.find('h1',class_='product-title').text.strip()
                data['available'] = soup.find('div',class_='order-box__availability').text.strip() == 'В наявності'
                data['price'] = ''.join([letter for letter in soup.find('div',class_='product-price__item').text.strip() if letter in '1234567890.'])
                data['description'] = f'<! [CDATA {str(descript)}]'
                data['img_list'] = ['https://opt-drop.com'+img.get('src') for img in img_list]
                data['category'] = soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[1].text.strip()
                data['category2'] = soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[2].text.strip() if soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[2] else ''
                data['category3'] = soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[3].text.strip() if len(soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')) >= 4 else ''
                data['category4'] = soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[4].text.strip() if len(soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')) >= 5 else ''
                data['category5'] = soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[5].text.strip() if len(soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')) >= 6 else ''
                # data['category5'] = soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[5].text.strip() if soup.find('nav',class_='breadcrumbs').find_all('div',class_='breadcrumbs-i')[5] else ''
                data['article'] = soup.find('div',class_='product-header__code').text.split(':')[1]

                if data['name'] == '': data['name'] = ''
            new_url = url.replace('https://opt-drop.com/','ru/')
            # https://opt-drop.com/ru/aksessuary-y-hadzhety-dlia-avto/4359/

            new_url = 'https://opt-drop.com/'+new_url
            async with session.get(new_url) as resp:
                soup = BeautifulSoup(await resp.text(), 'lxml')
                data['name_ru'] = soup.find('h1', class_='product-title').text.strip()
                descript = soup.find('div', class_='product-description').findChildren() if soup.find('div',
                                                                                                      class_='product-description') else ' '
                data['description_ru'] = f'<! [CDATA {str(descript)}]'
            return data

    except Exception as e:
        print('parser error ',url,'error id -',e)
        return 'nothing here'



async def main():


    tasks = []
    id = 0
    connection = sqlite3.connect('db/my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    url TEXT NOT NULL,
    available BOOLEAN,
    category TEXT,
    category2 TEXT,
    category3 TEXT,
    category4 TEXT,
    category5 TEXT,
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
    img_ten TEXT,
    article TEXT,
    name_ru TEXT,
    description_ru TEXT
    )
    ''')
    cursor.execute("""SELECT url FROM products""")
    urls = cursor.fetchall()
    urls = [url[0] for url in urls]
    print('len urls - ',len(urls), 'https://opt-drop.com/tekstyl/4774/' in urls)
    with open('data/catalog.txt') as file:
        for row in file.readlines():
            row.strip()
            if row.strip() in urls:
                id += 1
                continue
            task = asyncio.create_task(scrape(row.strip()))
            tasks.append(task)

        print('total counter of urls - ',id)
    data = await asyncio.gather(*tasks)
    print('created')
    for item in data:
        if item == 'nothing here':
            continue
        pprint(item)
        # if item['name'] == None or item['name'] == '' or not item['name']:
        try:
            cursor.execute('INSERT INTO products (name, url, available,category,category2,category3,category4,category5,description,price,img_one,img_two,img_three,img_four,img_five,img_six,img_seven,img_eight,img_nine,img_ten,article,name_ru,description_ru) VALUES (?,?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?, ? ,? ,?, ? ,? ,?, ? ,? ,?)', (
                item['name'],
                item['url'],
                item['available'],
                item['category'],
                item['category2'],
                item['category3'],
                item['category4'],
                item['category5'],
                item['description'],
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
                item['img_list'][9] if len(item['img_list']) > 10 else '',
                item['article'],
                item['name_ru'],
                item['description_ru']


                ))
        except Exception as e:
            print('err while appending this item - ',e,item)
    connection.commit()
    connection.close()


def scraping_catalogue():
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(time.time() - start_time)