from django.conf.urls import include, url
from . import views

app_name = 'search'

urlpatterns = [
    # DEFAULT SEARCH RESULTS PAGE
    url(r'^$', views.search, name='search'),
    # FILTERED SEARCH PAGE
    url(r'^sex_(?P<sex>[\w-]+)_cat_(?P<category>[ \w-]+)_size_(?P<size>[\w-]+)', views.search, name='search'),
]
