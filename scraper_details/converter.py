import sqlite3
import pprint
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime
import os
from dotenv import load_dotenv
import random

def convert():
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


    connection = sqlite3.connect('db/my_database.db')
    cursor = connection.cursor()

    # listOfCat = ['Новинки','Для дома и сада',"Красота и здоровье","Товары для детей","Отдый и туризм","Товары для спорта","Одежда, обувь и аксессуары","Автотовары","Зоотовары","Техника и электроника","Лсвещение","Охранные системы и сигнализации","Системы видеонаблюдения","Громкоговорители","Детекторы банкнот","Подарки","Новый год и Рождество","Дополнитьельный раздел",'Освещение','Отдых и туризм']
    # cursor.execute('SELECT category FROM products')
    # categories = list(set(cursor.fetchall()))
    # listOfCat = [cat[0] for cat in categories]
    # # print(listOfCat)
    categories = SubElement(shop, 'categories')
    # for i in range(len(listOfCat)):
    #     cat = SubElement(categories, 'category',attrib={'id':str(i)})
    #     cat.text = listOfCat[i]


    cursor.execute('SELECT category,category2,category3,category4,category5 FROM products')
    categories2 = cursor.fetchall()
    categ1 = {}
    categ2 = {}
    categ3 = {}
    categ4 = {}
    categ5 = {}
    indexation = 0
    for category2 in categories2:
        for catet in range(len(category2)):
            # print(category2[catet],end=' ')
            if catet == 0:
                if category2[catet] not in list(categ1.keys()):
                    indexation += 1
                    categ1[category2[catet]] = str(indexation)

                    cat = SubElement(categories, 'category',attrib={'id':str(indexation)})

                    cat.text = category2[catet]
            if catet == 1:
                if category2[catet] != '' and category2[catet] not in list(categ2.keys()):
                    indexation += 1
                    categ2[category2[catet]] = str(indexation)

                    cat = SubElement(categories, 'category', attrib={'id': str(indexation),'parentId':categ1[category2[catet-1]]})
                    cat.text = category2[catet]

            if catet == 2:
                if category2[catet] != '' and category2[catet] not in list(categ3.keys()):
                    indexation += 1
                    categ3[category2[catet]] = str(indexation)

                    cat = SubElement(categories, 'category',
                                     attrib={'id': str(indexation), 'parentId': categ2[category2[catet - 1]]})
                    cat.text = category2[catet]
            if catet == 3:
                if category2[catet] != '' and category2[catet] not in list(categ4.keys()):
                    indexation += 1
                    categ4[category2[catet]] = str(indexation)

                    cat = SubElement(categories, 'category',
                                     attrib={'id': str(indexation), 'parentId': categ3[category2[catet - 1]]})
                    cat.text = category2[catet]
            if catet == 4:
                if category2[catet] != '' and category2[catet] not in list(categ5.keys()):
                    indexation += 1
                    categ5[category2[catet]] = str(indexation)

                    cat = SubElement(categories, 'category',
                                     attrib={'id': str(indexation), 'parentId': categ4[category2[catet - 1]]})
                    cat.text = category2[catet]
        # print()
    # print(categ1)
    # print(categ2)
    # print(categ3)
    # print(categ4)
    # print(categ5)
    emptyVal = []
    emptyVal+=list(categ1.values())
    emptyVal+=list(categ2.values())
    emptyVal+=list(categ3.values())
    emptyVal+=list(categ4.values())
    emptyVal+=list(categ5.values())
    print(len(emptyVal),emptyVal)

    counter = 0




    cursor.execute('SELECT * FROM products')
    users = cursor.fetchall()

    offers = SubElement(shop, 'offers')
    for user in users:
        if not user[10] or not user[11]:
            continue
        counter+=1
        # print(user)
        offer = SubElement(offers, 'offer',attrib={'id':str(user[0]),'available':'true' if user[3] == 1 else 'false','selling_type':'r'})
        name = SubElement(offer, 'name_ua')
        name.text = user[1] if user[1] else 'Товар'
        nameRu = SubElement(offer, 'name')
        nameRu.text = user[22] if user[22] else 'Товар'
        description = SubElement(offer, 'description_ua')
        description.text = user[9]
        descriptionRu = SubElement(offer, 'description')
        descriptionRu.text = user[23]
        vendorCode = SubElement(offer, 'vendorCode')
        vendorCode.text = str(user[21])
        offerUrl = SubElement(offer, 'url')
        offerUrl.text = str(user[2])
        currencyId = SubElement(offer, 'currencyId')
        currencyId.text = 'UAH'
        categoryId = SubElement(offer, 'categoryId')

        cType = 10

        categoryId.text = str(f'{categ1[user[4]]}')
        if user[5] != '':
            categoryId.text = str(f'{categ2[user[5]]}')
        if user[6] != '':
            categoryId.text = str(f'{categ3[user[6]]}')
        if user[7] != '':
            categoryId.text = str(f'{categ4[user[7]]}')
        if user[8] != '':
            categoryId.text = str(f'{categ5[user[8]]}')
        # print(categoryId.text)
        if categoryId.text in emptyVal:
            emptyVal.pop(emptyVal.index(categoryId.text))
        price = SubElement(offer, 'price')
        price.text = str(user[10])
        for i in range(11,20):
            if user[i] == '': break
            img = SubElement(offer,'picture')
            img.text = user[i]
        vendor = SubElement(offer, 'vendor')
        vendor.text = 'opt-drop'



        # quantity_in_stock = SubElement(offer, 'quantity_in_stock')
        # quantity_in_stock.text = '15'
    print(len(emptyVal), emptyVal)
    for user in users:
        if not user[10] or not user[11]:
            continue

        if str(f'{categ1[user[4]]}') in emptyVal and user[3] == 1:
            counter += 1
            emptyVal.remove(str(f'{categ1[user[4]]}'))
            offer = SubElement(offers, 'offer',
                               attrib={'id': '123'+str(user[0]), 'available': 'true' if user[3] == 1 else 'false',
                                       'selling_type': 'r'})
            name = SubElement(offer, 'name_ua')
            name.text = user[1] if user[1] else 'Товар'
            nameRu = SubElement(offer, 'name')
            nameRu.text = user[22] if user[22] else 'Товар'
            description = SubElement(offer, 'description_ua')
            description.text = user[9]
            descriptionRu = SubElement(offer, 'description')
            descriptionRu.text = user[23]

            vendorCode = SubElement(offer, 'vendorCode')
            vendorCode.text = str(user[21])
            offerUrl = SubElement(offer, 'url')
            offerUrl.text = str(user[2])
            currencyId = SubElement(offer, 'currencyId')
            currencyId.text = 'UAH'

            categoryId = SubElement(offer, 'categoryId')
            categoryId.text = str(f'{categ1[user[4]]}')
            # print(categoryId.text)
            if categoryId.text in emptyVal:
                emptyVal.pop(emptyVal.index(categoryId.text))
            price = SubElement(offer, 'price')
            price.text = str(user[10])
            for i in range(11, 20):
                if user[i] == '': break
                img = SubElement(offer, 'picture')
                img.text = user[i]
            vendor = SubElement(offer, 'vendor')
            vendor.text = 'opt-drop'

    for user in users:
        if not user[10] or not  user[11]:
            continue

        if str(f'{categ2[user[5]]}') in emptyVal and user[3] == 1:
            counter += 1
            emptyVal.remove(str(f'{categ2[user[5]]}'))
            offer = SubElement(offers, 'offer',
                               attrib={'id': '223'+str(user[0]), 'available': 'true' if user[3] == 1 else 'false',
                                       'selling_type': 'r'})
            name = SubElement(offer, 'name_ua')
            name.text = user[1] if user[1] else 'Товар'
            nameRu = SubElement(offer, 'name')
            nameRu.text = user[22] if user[22] else 'Товар'
            description = SubElement(offer, 'description_ua')
            description.text = user[9]
            descriptionRu = SubElement(offer, 'description')
            descriptionRu.text = user[23]

            vendorCode = SubElement(offer, 'vendorCode')
            vendorCode.text = str(user[21])
            offerUrl = SubElement(offer, 'url')
            offerUrl.text = str(user[2])
            currencyId = SubElement(offer, 'currencyId')
            currencyId.text = 'UAH'

            cType = 10
            categoryId = SubElement(offer, 'categoryId')
            categoryId.text = str(f'{categ2[user[5]]}')
            # print(categoryId.text)
            if categoryId.text in emptyVal:
                emptyVal.pop(emptyVal.index(categoryId.text))
            price = SubElement(offer, 'price')
            price.text = str(user[10])
            for i in range(11, 20):
                if user[i] == '': break
                img = SubElement(offer, 'picture')
                img.text = user[i]
            vendor = SubElement(offer, 'vendor')
            vendor.text = 'opt-drop'

    print(len(emptyVal), emptyVal)
    print('coutner',counter)

        # print(categoryId.text)
        # if categoryId.text in emptyVal:
        #     emptyVal.pop(emptyVal.index(categoryId.text))


    connection.commit()
    connection.close()

    # print(tostring(top,encoding='utf-8').decode('utf-8'))
    xml_file = open('result.xml','w',encoding='UTF-8')
    xml_file.write(tostring(top,encoding='utf-8').decode(encoding='utf-8'))
    xml_file.close()