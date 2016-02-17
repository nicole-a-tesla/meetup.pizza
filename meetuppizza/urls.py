from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    url(r'^$', 'meetuppizza.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
]
