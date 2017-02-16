from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

handler400 = 'xsd_frontend.views.handler400'
handler403 = 'xsd_frontend.views.handler403'
handler404 = 'xsd_frontend.views.handler404'
handler500 = 'xsd_frontend.views.handler500'

urlpatterns = patterns('',
                       url(r'^update-request/$', 'xsd_frontend.views.update_request', name='update_request'),

                       url(r'^design/$', 'xsd_frontend.views.design', name='design'),

                       url(r'^', include('xsd_frontend.urls', namespace='xsd_frontend')),

                       url(r'^members/', include('xsd_members.urls', namespace='xsd_members')),

                       url(r'^training/', include('xsd_training.urls', namespace='xsd_training')),

                       url(r'^sites/', include('xsd_sites.urls', namespace='xsd_sites')),

                       url(r'^trips/', include('xsd_trips.urls', namespace='xsd_trips')),

                       url(r'^kit/', include('xsd_kit.urls', namespace='xsd_kit')),

                       url(r'^about/', include('xsd_about.urls', namespace='xsd_about')),
                       url(r'^about/rq/', include('django_rq.urls')),

                       url(r'^help/', include('xsd_help.urls', namespace='xsd_help')),

                       # Bodge here as accounts/ URLS need to be avaliable under the xsd_auth
                       # namespace along with no namespace for access via external libs #185
                       url(r'^accounts/', include('allauth.urls', namespace='xsd_auth')),
                       url(r'^accounts/', include('allauth.urls')),

                       url(r'^hijack/', include('hijack.urls')),

                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^health/', include('health_check.urls')),

                       url(r'^404/$', 'django.views.defaults.page_not_found'),
                       )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]