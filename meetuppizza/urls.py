from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

import meetuppizza.views

urlpatterns = [
    url(r'^$', meetuppizza.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sign_up', meetuppizza.views.sign_up, name='sign_up'),
    url(r'^sign_out', meetuppizza.views.sign_out, name='sign_out'),
    url(r'^sign_in', meetuppizza.views.sign_in, name='sign_in')

]
