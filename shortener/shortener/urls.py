# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns('',
    # admin app
    url(r'^admin/', include(admin.site.urls)),
    
    # accounts app
    url(r'^entrar/$', 'accounts.views.login', name='accounts_login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'next_page': '/',}, name='accounts_logout'),
    url(r'^cadastro/$', 'accounts.views.register', name='accounts_register'),
    
    # shorturl app
    url(r'^$', 'shorturl.views.index', name='shorturl_index'),
    url(r'^link/encurtar/$', 'shorturl.views.add_link', name='shorturl_add_link'),
    url(r'^link/(?P<id>\d+)/$', 'shorturl.views.show_link', name='shorturl_show_link'),
    url(r'^meus-links/$', 'shorturl.views.my_links', name='shorturl_my_links'),
    url(r'^(?P<base_62>\w+)/$', 'shorturl.views.redirect_link', name='shorturl_redirect_link'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )


urlpatterns += staticfiles_urlpatterns()
