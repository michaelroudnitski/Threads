# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import generic
import operator
import re
from django.db.models import Q
from .models import Sex, Category, Product

mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}

def index(request):
    """
    View request for index page of catalog
    """
    MEN = Sex.objects.get(sex_selection='m')
    WOMEN = Sex.objects.get(sex_selection='w')
    context = {'sex': ['m','w']}
    context.update(cat_context)
    return render(request, 'catalog/index.html', context)


def about(request):
    """
    View request for about us page of catalog
    """
    #context = cat_context
    return render(request, 'catalog/about_us.html')


def mw(request, selection):
    """
    View request for sex (mens or womens) page of catalog
    """
    try:
        selected = Sex.objects.get(sex_selection=selection)
        cata = selected.category_set.all()
        products = Product.objects.all()
        products = products.filter(category__sex__sex_selection = selection)
    except Sex.DoesNotExist:
        raise Http404("Invalid selection")
    context = {'selection': selection, 'selected': selected, 'cata':cata, 'products': products}
    context.update(cat_context)
    return render(request, 'catalog/sex.html', context)


def products_list(request, selection, category):
    """
    View request to display products under a selected category
    :param selection: sex selected
    :param category: category selected
    :return: product list template
    """
    selected = Sex.objects.get(sex_selection=selection)
    products = Sex.objects.all()
    try:
        category_selected = Category.objects.get(sex=selected, name=category)
        items = category_selected.product_set.all()
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    context = {'items': items, 'category': category, 'selected': selected}
    context.update(cat_context)
    return render(request, 'catalog/products.html', context=context)


def product(request, p_id):
    """
    View request displaying html template for a selected product
    :param prod_id: product id given
    :return: product page template
    """
    try:
        product = Product.objects.get(id=p_id)
    except Product.DoesNotExist:
        raise Http404("Product is not in our system!")
    context = {'product': product}
    context.update(cat_context)
    return render(request, 'catalog/product_info.html', context)


def search(request, sex='mw', category='all_products', size='all_size', page=1):
    available_categories = Category.objects.values_list('name', flat=True)
    search_query = request.GET.get("q", '')
    available_sizes = ['stockXL', 'stockL', 'stockM', 'stockS']

    if request.method == 'GET':  # If the form is submitted
        queryset_list = Product.objects.all()
        new_queryset_list = []
        # If search query is not empty

        if search_query:
            if str(search_query) not in "1234567890":
                keywords = re.split(' ,-', search_query)

                if sex != 'mw':
                    queryset_list = queryset_list.filter(category__sex__sex_selection=sex)

                elif category != 'all_products':
                    queryset_list = queryset_list.filter(category__name=category)

                elif size != 'all_size':
                    for i in queryset_list:
                        sizes_dic = {'stockXL': i.stockXL, 'stockL': i.stockL, 'stockM': i.stockM, 'stockS': i.stockS}
                        if sizes_dic[size] > 0:
                            new_queryset_list.append(i)

                queryset_list = queryset_list.filter(
                    reduce(operator.or_,
                           (Q(name__icontains=keyword) for keyword in keywords)) |
                    reduce(operator.and_,
                           (Q(category__name__icontains=keyword) for keyword in keywords))
                )

            else:
                queryset_list = queryset_list.filter(id=int(search_query))
        # -----------------------------
        else:
            search_query = 'all products'

        if len(new_queryset_list) !=0:
            queryset_list = new_queryset_list

        if len(queryset_list) != 0:
            search_message = ""
        else:
            search_message = "No Result"

        amount_product = 3
        to_number = amount_product*int(page)
        from_number = to_number-amount_product

        amount_of_page = len(queryset_list)/amount_product +1
        list_page = []

        for i in range(amount_of_page):
            list_page.append(i+1)

        context = {'queryset_list': queryset_list[from_number:to_number],
                   'search_query': search_query,
                   'category': category,
                   'size': size,
                   'page': page,
                   'list_page': list_page,
                   'selected_sex': sex,
                   "search_message": search_message,
                   'categories': set(available_categories),
                   'sizes': set(available_sizes)}
        context.update(cat_context)

        return render(request, 'catalog/search_info.html', context)
