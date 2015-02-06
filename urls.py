from django.conf.urls import patterns, include, url
#from django.views.generic.base import TemplateView
from django.http import HttpResponse
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^pic/(?P<url>.*)$', 'util.web_helpers.pic_csrf.pic_csrf', name='pic_csrf'),
    #url(r'^$', 'apps.cc.views.index', name='index'),
    url(r'^$', 'apps.cc.views.index', name='index'),
    url(r'^api$', 'apps.cc.views.api', name='api'),
    url(r'^url/(?P<id>\d+)/delete$', 'apps.cc.views.delete', name='delete'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^500/$', 'util.web_helpers.error_page.server_error_500', name='server_error_500'),
    url(r'^404/$', 'util.web_helpers.error_page.server_error_404', name='server_error_404'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT }),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)

handler404 = 'util.web_helpers.error_page.server_error_404'
handler404 = 'util.web_helpers.error_page.server_error_500'