# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# There are 3 main classes/*tables*
# The Sex class creates a table with two rows, mens and womens
# The Category class creates a table with rows corresponding to each category in our database
#   Each row has columns that contain it's assigned sex and just the name
# The Product class creates a table with rows corresponding to each product in our database
#   Each row has columns that contain assigned category, name, price, etc...

class Sex(models.Model):
    """model for mens/womens"""
    MENS = 'm'
    WOMENS = 'w'
    # Django has documentation on choice fields, read that
    sex_choices = (
        (MENS, "MENS"),
        (WOMENS, "WOMENS")
    )
    sex_selection = models.CharField(max_length=5, choices=sex_choices, default=MENS)

    def __str__(self):
        return self.get_sex_selection_display()


class Category(models.Model):
    """model for categories"""
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name + '  ' + str(self.sex)


class Product(models.Model):
    """model for a product"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    rating = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(5)], default=0)    # This has not been finished yet, make it so that users can use sessions to enter a product review
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # Sale price is 0 by default so when the system detects it's any value between 0 and it's regular price, it displays sale price
    thumbnail_image = models.CharField(max_length=1000, default="/static/catalog/images/Placeholder.jpg")
    description = models.CharField(max_length=1500, default="There is no description available at the moment")
    stockXL = models.IntegerField(default=0)
    stockL = models.IntegerField(default=0)
    stockM = models.IntegerField(default=0)
    stockS = models.IntegerField(default=0)
    featured = models.IntegerField(default=0, validators = [MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return self.name + ' - ' + self.category.name + ' - ' + str(self.category.sex)


class ProductImage(models.Model):
    """Child model for images going into a product
        This is a many to one relationship using ForeignKey"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # This ForeignKey assigns the object to a parent product object
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.product.name

# manage.py shell
# from (appname).models import Category
