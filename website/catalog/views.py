# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from catalog.models import Sex, Category, Product, ProductImage
from django.shortcuts import redirect

# make this block of code a global function so it doesnt need to be repeated everytime
mcata = Sex.objects.get(sex_selection='m').category_set.all()
wcata = Sex.objects.get(sex_selection='w').category_set.all()
cat_context = {'mcata': mcata, 'wcata': wcata}
######################################################################################

def index(request):
    """View request for index page of catalog"""
    MEN = Sex.objects.get(sex_selection='m')
    WOMEN = Sex.objects.get(sex_selection='w')
    featured_list = Product.objects.filter(featured=1)
    context = {'sex': ['m','w'],
               'featured_list': featured_list}
    context.update(cat_context) # this line adds all our category information to the page, it's necessary for our Men's/Women's dropdowns
    return render(request, 'catalog/index.html', context)


def about(request):
    """View request for about us page of catalog"""
    context = cat_context
    return render(request, 'catalog/about_us.html', context)


def mw(request, selection, order='name', order_type='asc'):
    """View request for sex (mens or womens) page of catalog"""
    try:
        selected = Sex.objects.get(sex_selection=selection)
        cata = selected.category_set.all()
        if order_type == 'asc':
            products = Product.objects.order_by(order)
        elif order_type == 'desc':
            products = Product.objects.order_by('-' + order)
        products = products.filter(category__sex__sex_selection = selection)

    except Sex.DoesNotExist:
        raise Http404("Invalid selection")

    if order_type =='asc':
        products = products.order_by(order)
    elif order_type =='desc':
        products = products.order_by('-'+order)

    page = request.GET.get('page', 1) # paginator
    paginator = Paginator(products, 16)
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

    context = {'selection': selection,
               'selected': selected,
               'cata':cata,
               'page_range': page_range,
               'page': page,
               'products': products,
               'order':order,
               'order_type':order_type,
               }
    context.update(cat_context)
    return render(request, 'catalog/sex.html', context)


def products_list(request, selection, category, order='name', order_type='asc'):
    """View request to display products under a selected category"""
    try:
        selected = Sex.objects.get(sex_selection=selection)
        products = Category.objects.get(sex=selected, name=category).product_set.all()
    except Category.DoesNotExist:
        raise Http404("Category does not exist")

    if order_type =='asc':
        products = products.order_by(order)
    elif order_type =='desc':
        products = products.order_by('-'+order)

    page = request.GET.get('page', 1) # paginator
    paginator = Paginator(products, 16)
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

    cata = Sex.objects.get(sex_selection=selection).category_set.all()
    context = {'page': page,
               'products': products,
               'page_range':page_range,
               'category': category,
               'selected': selected,
               'cata':cata,
               'order': order,
               'order_type': order_type,
               }
    context.update(cat_context)
    return render(request, 'catalog/products.html', context=context)


def product(request, p_id, thumbnail_image='None'):
    """View request displaying html template for a selected product"""
    try:
        product = Product.objects.get(id=p_id)
        prodImages = ProductImage.objects.filter(product=p_id).select_related()
    except Product.DoesNotExist:
        raise Http404("Product is not in our system")
    if thumbnail_image == 'None':
        thumbnail_image = product.thumbnail_image
    else:
        thumbnail_image = ProductImage.objects.get(id=thumbnail_image).image

    if product.sale_price > 0:
        cart_price = product.sale_price
    else:
        cart_price = product.price

    if request.method == 'POST':    # check if form is submitted
        if 'add_to_cart' in request.POST:   # if the form was the add to cart form
            cart = request.session.get('cart', {})  # add to item to our cart dictionary
            cart[p_id] = (product.thumbnail_image, product.name, str(cart_price), request.POST.get('size_selection'), request.POST.get('quantity'))
            request.session['cart'] = cart
            return redirect('catalog:cart_confirmation', p_id=p_id) # redirects to page showing confirmation of cart addition

    related_products = Category.objects.get(sex=product.category.sex, name=product.category.name).product_set.all().exclude(id=p_id)
    related_products = related_products[:8]

    context = {'product': product,
                'prodImages': prodImages,
                'p_list':related_products,
                'thumbnail_image':thumbnail_image}
    context.update(cat_context)
    return render(request, 'catalog/product_info.html', context)


def get_cart(request):
    """View function for the user's cart"""
    cart_items = request.session.get('cart', {})
    subtotal = 0
    total = 0
    if request.method == 'POST': # Same formula as add to cart, just opposite
        if 'remove_from_cart' in request.POST:
            cart = request.session.get('cart', {})
            del cart[request.POST.get('p_id')]
            request.session['cart'] = cart

    cart = request.session.get('cart', {})
    for item in cart:
        subtotal += float(cart[item][2])*int(cart[item][4])
    total = round(subtotal*1.13,2)
    tax = total-subtotal

    context = {'cart_items': cart_items,
               'subtotal': subtotal,
               'total': total,
               'tax': tax}
    context.update(cat_context)
    return render(request, 'catalog/cart.html', context)


def cart_confirmation(request, p_id):
    """The page a user sees after adding an item to their cart"""
    try:
        product = Product.objects.get(id=p_id)
    except Product.DoesNotExist:
        raise Http404("Invalid product selection")

    related_products = Category.objects.get(sex=product.category.sex, name=product.category.name).product_set.all().exclude(id=p_id)
    related_products = related_products[:5]
    context = {'product': product,
               'p_list':related_products,}
    context.update(cat_context)
    return render(request, 'catalog/cart_confirmation.html', context)
