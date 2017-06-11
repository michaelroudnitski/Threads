# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import operator, re
from django.views import generic
from django.db.models import Q
from catalog.models import Sex, Category, Product
from django.http import HttpResponse, Http404
from django.shortcuts import render

mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}


def search(request, sex='mw', category='all_products', size='all_size'):
    available_categories = Category.objects.values_list('name', flat=True)
    search_query = request.GET.get("q", '')
    new_queryset_list = []
    available_sizes = ['stockXL', 'stockL', 'stockM', 'stockS']
    page = request.GET.get('page', 1) # paginator
    queryset_list = Product.objects.all()

    if sex != 'mw': # if field is not default
        queryset_list = queryset_list.filter(category__sex__sex_selection=sex)

    elif category != 'all_products':
        queryset_list = queryset_list.filter(category__name=category)

    elif size != 'all_size':
        for i in queryset_list:
            sizes_dic = {'stockXL': i.stockXL, 'stockL': i.stockL, 'stockM': i.stockM, 'stockS': i.stockS}
            if sizes_dic[size] > 0:
                new_queryset_list.append(i)

    if request.method == 'GET':  # If the form is submitted
        if search_query: # If search query is not empty
            if str(search_query) not in "1234567890": # If the search query is not entirely composed of integers
                keywords = search_query.split()
                queryset_list = queryset_list.filter(
                    reduce(operator.or_,
                           (Q(name__icontains=keyword) for keyword in keywords)) |
                    reduce(operator.and_,
                           (Q(category__name__icontains=keyword) for keyword in keywords))
                )

            else: # The search query is entirely composed of integers - find item by id
                queryset_list = queryset_list.filter(id=int(search_query))

        else: #if search query is empty
            search_query = 'all products' # Display all products

        if len(new_queryset_list) !=0:
            queryset_list = new_queryset_list

        paginator = Paginator(queryset_list, 1)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        # Get the index of the current page
        index = products.number - 1  # edited to something easier without index
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        # My new page range

        page_range = list(paginator.page_range)
        page_range = page_range[start_index:end_index]

        amount_of_results = len(queryset_list)

        context = {'amount_of_results': amount_of_results,
                   'search_query': search_query,
                   'category': category,
                   'size': size,
                   'page': page,
                   'products': products,
                   'page_range':page_range,
                   'selected_sex': sex,
                   'categories': sorted(set(available_categories)),
                   'sizes': available_sizes}
        context.update(cat_context)

        return render(request, 'search/search_info.html', context)
