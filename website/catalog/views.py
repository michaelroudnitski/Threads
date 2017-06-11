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
               'featured_list': featured_list,}
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
    except Product.DoesNotExist:
        raise Http404("Product is not in our system")
    if product.sale_price > 0:
        cart_price = product.sale_price
    else:
        cart_price = product.price

    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            cart = request.session.get('cart', {})
            cart[p_id] = (product.thumbnail_image, product.name, str(cart_price), request.POST.get('size_selection'), request.POST.get('quantity'))
            request.session['cart'] = cart

    context = {'product': product, 'prodImages': prodImages}
    context.update(cat_context)
    return render(request, 'catalog/product_info.html', context)


def get_cart(request):
    cart_items = request.session.get('cart', {})
    subtotal = 0
    total = 0
    if request.method == 'POST':
        if 'remove_from_cart' in request.POST:
            cart = request.session.get('cart', {})
            del cart[request.POST.get('p_id')]
            request.session['cart'] = cart

    cart = request.session.get('cart', {})
    for item in cart:
        subtotal += float(cart[item][2])
    total = round(subtotal*1.13,2)
    tax = total-subtotal

    context = {'cart_items': cart_items,
               'subtotal': subtotal,
               'total': total,
               'tax': tax}
    context.update(cat_context)
    return render(request, 'catalog/cart.html', context)
