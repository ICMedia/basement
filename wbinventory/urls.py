from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.views.generic import TemplateView
from invent import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.ItemListView.as_view(), name='itemlistview'),
    url(r'^item/(?P<slug>[-_\w]+)/$', views.ItemView.as_view(), name='itemview'),
    url(r'^admin/', include(admin.site.urls)),
)
