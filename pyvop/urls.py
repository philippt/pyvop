from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pyvop.views.home', name='home'),
    #url(r'^pyvop/', include('pyvop.foo.urls')),
    url(r'^foo/status/(.+)$', 'foo.views.status'),
    url(r'^foo/machine/(.+)$', 'foo.views.machine'),
    url(r'^foo/map$', 'foo.views.map'),
    url(r'^foo/list$', 'foo.views.list'),
    url(r'^foo/$', 'foo.views.index'),
    #url(r'^.+$', 'foo.views.index'),
    
    url(r'^machines.json$', 'foo.views.machines'),
    
    url(r'^.*$', 'foo.views.public'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
