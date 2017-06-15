from django.conf.urls import include, url
from . import views

app_name = 'catalog'
# r'^(?P<selection>[\w-]+)/$' is a *regular expression* looking for string values
urlpatterns = [

    url(r'^catalog/', include([

        url(r'^$', views.index, name='index'),

        # MENS/WOMENS CATEGORY SELECTION PAGE
        url(r'^(?P<selection>[\w-]+)/$', views.mw, name='mw'),

        # MENS/WOMENS CATEGORY SELECTION PAGE
        url(r'^(?P<selection>[\w-]+)/(?P<order>[\w-]+)/(?P<order_type>[\w-]+)/$', views.mw, name='mw_with_sort'),

        # CATEGORY PAGE DISPLAYING PRODUCTS
        url(r'^(?P<selection>[\w-]+)/(?P<category>[ \w-]+)/$', views.products_list, name='products_list'),

        # CATEGORY PAGE DISPLAYING PRODUCTS WITH SORT
        url(r'^(?P<selection>[\w-]+)/(?P<category>[ \w-]+)/(?P<order>[\w-]+)/(?P<order_type>[\w-]+)/$', views.products_list, name='products_list_with_sort'),

        ])),

    # PRODUCT PAGE DISPLAYING PRODUCT INFO
    url(r'^(?P<p_id>[0-9]+)/$', views.product, name='prod'),

    # PRODUCT PAGE DISPLAYING PRODUCT INFO
    url(r'^(?P<p_id>[0-9]+)/(?P<thumbnail_image>[ \d-]+)/$', views.product, name='prod'),

    # ITEM ADDED TO CART CONFIRMATION PAGE
    url(r'^cart/cart_confirmation/(?P<p_id>[0-9]+)/$', views.cart_confirmation, name='cart_confirmation'),

    # CART PAGE
    url(r'^cart/$', views.get_cart, name='get_cart'),

    # ABOUT US
    url(r'^about/', views.about, name='about'),

    # HOME PAGE
    url(r'^$', views.index, name='index'),

]
