from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import meetuppizza.views

urlpatterns = [
    url(r'^$', meetuppizza.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sign_up', meetuppizza.views.sign_up, name='sign_up'),
    url(r'^welcome', meetuppizza.views.welcome, name='welcome'),

]