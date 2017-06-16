from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

app_name = 'account'

urlpatterns = [
    # Format of URL
    # url(r'^name_of_url/$', file that show view, name='name of this url'),

    # URL to register page
    url(r'^register/$', views.register, name='register'),

    # URL to login page
    url(r'^$', login, {'template_name': 'account/index.html'}, name='index'),

    # URL to profile page
    url(r'^profile/$', views.profile, name='profile'),

    # URL to edit profile page
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),

    # URL to logout page
    url(r'^logout/$', views.logout_view, name='logout_view'),

    # URL to password change page
    url(r'^profile/password/$', views.change_password, name='change_password'),

    # URL to delete account page
    url(r'^delete-account/$', views.del_user, name='del_user'),

    # URL to reset password page
    url(r'^reset-password/$', password_reset, {'template_name': 'account/reset_password.html', 'post_reset_redirect': 'account:password_reset_done', 'email_template_name': 'account/reset_password_email.html'}, name='reset_password'),

    # URL to reset password done page
    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'account/reset_password_done.html'}, name='password_reset_done'),

    # URL to reset password confirm page
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'account/reset_password_confirm.html', 'post_reset_redirect': 'account:password_reset_complete'}, name='password_reset_confirm'),

    # URL to reset password complete page
    url(r'^reset-password/complete/$', password_reset_complete,{'template_name': 'account/reset_password_complete.html'}, name='password_reset_complete'),

]
##python -m smtpd -n -c DebuggingServer localhost:1025
