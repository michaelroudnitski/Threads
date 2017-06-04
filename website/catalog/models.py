# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Sex(models.Model):
    """
    model for mens/womens
    """
    MENS = 'm'
    WOMENS = 'w'
    sex_choices = (
        (MENS, "MENS"),
        (WOMENS, "WOMENS")
    )
    sex_selection = models.CharField(max_length=5, choices=sex_choices, default= MENS)

    def __str__(self):
        return self.get_sex_selection_display()


class Category(models.Model):
    """
    model for categories
    """
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name + '  ' + str(self.sex)


class Product(models.Model):
    """
    model for a product
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    rating = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(5)], default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    thumbnail = models.CharField(max_length=1000, default="/static/catalog/images/Placeholder.jpg")
    description = models.CharField(max_length=1500, default="There is no description available at the moment")
    stockXL = models.IntegerField(default=0)
    stockL = models.IntegerField(default=0)
    stockM = models.IntegerField(default=0)
    stockS = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ' - ' + self.category.name + ' - ' + str(self.category.sex)
# manage.py shell
# from (appname).models import Category
