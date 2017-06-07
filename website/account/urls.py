from django.conf.urls import url
from . import views
from django.contrib.auth.views import login

app_name = 'account'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^$', login, {'template_name': 'account/index.html'}, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit$', views.edit_profile, name='edit_profile'),
    url(r'^logout$', views.logout_view, name='logout_view'),
]
