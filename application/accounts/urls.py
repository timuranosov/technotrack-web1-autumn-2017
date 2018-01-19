from django.conf.urls import url
from accounts.views import signup
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'home.html'}, name='logout')
]


