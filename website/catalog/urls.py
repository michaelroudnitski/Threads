from django.conf.urls import include, url
from . import views

app_name = 'catalog'

urlpatterns = [

    url(r'^catalog/', include([

        url(r'^$', views.index, name='index'),

        # MENS/WOMENS CATEGORY SELECTION PAGE
        url(r'^(?P<selection>[\w-]+)/$', views.mw, name='mw'),

        # CATEGORY PAGE DISPLAYING PRODUCTS
        url(r'^(?P<selection>[\w-]+)/(?P<category>[ \w-]+)/$', views.products_list, name='products_list'),

        ])),

    # PRODUCT PAGE DISPLAYING PRODUCT INFO
    url(r'^(?P<p_id>[0-9]+)/$', views.product, name='prod'),

    # ABOUT US
    url(r'^about/', views.about, name='about'),

    # HOME PAGE
    url(r'^$', views.index, name='index'),

]
