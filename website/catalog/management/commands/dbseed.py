from django.core.management.base import BaseCommand, CommandError
from catalog.models import Sex, Category, Product
import sys
import random

class Command(BaseCommand):
    help = 'Populates the database'
    def handle(self, *args, **options):
        try:
            num = input("Enter number of *random* items to populate database: ")
        except:
            sys.exit('input requires an integer value')
        confirm = raw_input("Are you sure you would like to populate the database? [y/n]: ")
        if confirm == 'y':
            charset = 'abcdefghijklmnopqrstuvxyz '
            for row in range(num):
                name = ''.join(random.choice(charset) for i in range(random.randint(2,20)))
                stockXL = random.randint(0,45)
                stockL = random.randint(0,45)
                stockM = random.randint(0,45)
                stockS = random.randint(0,45)
                category_id = random.randint(2,6)
                price = random.uniform(10.00, 150.00)
                price = float("{0:.2f}".format(price))
                if category_id != 5: # Remove category IDs that are not in our database otherwise things go to shit
                    p = Product(name=name, stockXL=stockXL, stockL=stockL, stockM=stockM, stockS=stockS, category_id=category_id, price=price)
                    p.save()
        elif confirm == 'n':
            sys.exit("No changes have been made to the database")
