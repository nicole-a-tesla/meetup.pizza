from django.conf.urls import include, url
from django.contrib import admin

import meetuppizza.views

urlpatterns = [
    url(r'^$', meetuppizza.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]
