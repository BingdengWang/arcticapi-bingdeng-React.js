#!/usr/bin/env python3

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcticapi.settings'
import django
django.setup()

# regular imports
from api.models import Category, Product
import json

# main script
def main():

    with open('products.json') as json_file:
        data = json.load(json_file)
    products = data['products']
    cats = []
    
    for prod in products:
        if prod["category"] in cats:
            dbcat = Category.objects.get(title=prod["category"])
            print('skip')
        else:
            dbcat = Category()
            dbcat.title = prod["category"]
            dbcat.save()
            cats.append(dbcat.title)
        dbprod = Product()
        dbprod.category = dbcat
        dbprod.name = prod["name"]
        dbprod.description = prod["description"]
        dbprod.price = prod["price"]
        dbprod.filename = prod["filename"]
        dbprod.save()


    # with open('products.json') as json_file:
    #     data = json.load(json_file)

    # products = data['products']
    # for prod in products:

    #     dbprod = Product()
    #     dbprod.category = Category.objects.get(title=prod['category'])
    #     dbprod.name = prod['name']
    #     dbprod.filename = prod['filename']
    #     dbprod.description = prod['description']
    #     dbprod.price = prod['price']
    #     dbprod.save()

# bootstrap
if __name__ == '__main__':
    main()





