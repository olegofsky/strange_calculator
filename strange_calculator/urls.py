from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'strange_calculator.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test/', include('calculator.urls')),
    url(r'^admin', include(admin.site.urls)),

)
