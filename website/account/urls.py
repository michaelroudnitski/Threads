from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'account'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^$', login, {'template_name': 'account/index.html'}, name='index'),
]
