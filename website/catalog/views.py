# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from catalog.models import Sex, Category, Product, ProductImage


mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}

def index(request):
    """
    View request for index page of catalog
    """
    MEN = Sex.objects.get(sex_selection='m')
    WOMEN = Sex.objects.get(sex_selection='w')
    featured_list = Product.objects.filter(featured=1)
    context = {'sex': ['m','w'],
               'featured_list': featured_list}
    context.update(cat_context)
    return render(request, 'catalog/index.html', context)


def about(request):
    """
    View request for about us page of catalog
    """
    context = cat_context
    return render(request, 'catalog/about_us.html', context)


def mw(request, selection):
    """
    View request for sex (mens or womens) page of catalog
    """
    try:
        selected = Sex.objects.get(sex_selection=selection)
        cata = selected.category_set.all()
        products = Product.objects.filter(category__sex__sex_selection = selection)
    except Sex.DoesNotExist:
        raise Http404("Invalid selection")

    page = request.GET.get('page', 1) # paginator
    paginator = Paginator(products, 16)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'selection': selection,
               'selected': selected,
               'cata':cata,
               'page': page,
               'products': products,}
    context.update(cat_context)
    return render(request, 'catalog/sex.html', context)


def products_list(request, selection, category):
    """
    View request to display products under a selected category
    """
    try:
        selected = Sex.objects.get(sex_selection=selection)
        products = Category.objects.get(sex=selected, name=category).product_set.all()
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    page = request.GET.get('page', 1) # paginator
    paginator = Paginator(products, 16)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    cata = Sex.objects.get(sex_selection=selection).category_set.all()
    context = {'page': page,
               'products': products,
               'category': category,
               'selected': selected,
               'cata':cata}
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
        prodImages = ProductImage.objects.filter(product=p_id).select_related()
        prodImages = list(prodImages).extend(product.thumbnail_image)
    except Product.DoesNotExist:
        raise Http404("Product is not in our system")
    context = {'product': product, 'prodImages': prodImages}
    context.update(cat_context)
    return render(request, 'catalog/product_info.html', context)
