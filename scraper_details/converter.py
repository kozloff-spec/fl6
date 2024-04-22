import sqlite3
import pprint
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime
import os
from dotenv import load_dotenv
import random

load_dotenv('config')
# print(os.getenv('name'))

top         = Element('yml_catalog',attrib={'date':str(datetime.now().strftime('%Y-%m-%d %H:%M'))})
shop       = SubElement(top, 'shop')
url         = SubElement(shop, 'url')
url.text = os.getenv('url')
name        = SubElement(shop, 'name')
name.text = os.getenv('name')
company     = SubElement(shop, 'company')
company.text = os.getenv('company')
phone       = SubElement(shop, 'phone')
phone.text = os.getenv('phone')

r = str(random.randint(10000000,99999999))
categories = SubElement(shop, 'categories')
cat1 = SubElement(categories, 'category',attrib={'id':r})
cat1.text = 'Зоотовары'

connection = sqlite3.connect('db/my_database.db')
cursor = connection.cursor()

cursor.execute('SELECT * FROM products')
users = cursor.fetchall()

offers = SubElement(shop, 'offers')
for user in users:
    print(user)
    offer = SubElement(offers, 'offer',attrib={'id':str(user[0]),'available':'true' if user[3] == 1 else 'false','selling_type':'r'})
    name = SubElement(offer, 'name')
    name.text = user[1]
    vendorCode = SubElement(offer, 'vendorCode')
    vendorCode.text = '111938'
    offerUrl = SubElement(offer, 'url')
    offerUrl.text = str(user[2])
    currencyId = SubElement(offer, 'currencyId')
    currencyId.text = 'UAH'
    categoryId = SubElement(offer, 'categoryId')
    categoryId.text = r
    price = SubElement(offer, 'price')
    price.text = str(user[6])
    for i in range(7,17):
        if user[i] == '': break
        img = SubElement(offer,'picture')
        img.text = user[i]
        print(user[i])
    vendor = SubElement(offer, 'vendor')
    vendor.text = 'opt-drop'
    description = SubElement(offer, 'description')
    description.text = user[5]
    quantity_in_stock = SubElement(offer, 'quantity_in_stock')
    quantity_in_stock.text = '15'


connection.commit()
connection.close()

# print(tostring(top,encoding='utf-8').decode('utf-8'))
xml_file = open('result.xml','w',encoding='UTF-8')
xml_file.write(tostring(top,encoding='utf-8').decode(encoding='utf-8'))
xml_file.close()