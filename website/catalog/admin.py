# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Sex, Category, Product, ProductImage

admin.site.register(Sex)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
