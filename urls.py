from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'scorekeeper.views.index'),
    (r'^game/(?P<game_slug>[-\w]+)/$', 'scorekeeper.views.game_detail'),
    (r'^ajax_game/(?P<game_slug>[-\w]+)/$', 'scorekeeper.views.ajax_game_detail'),
    (r'^level/(?P<level_slug>[-\w]+)/$', 'scorekeeper.views.level_detail'),
    (r'^player/(?P<player_slug>[-\w]+)/$', 'scorekeeper.views.player_detail'),
    (r'^score/$', 'scorekeeper.views.score'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
