from django.conf.urls import patterns, url

from calculator import views

urlpatterns = patterns('',

    url(r'^$', views.main, name='main'),
    url(r'^ajax', views.ajax, name='ajax'),
)
