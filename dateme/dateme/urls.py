from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dateme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dateme_app/', include('dateme_app.urls', namespace='dateme_app')),    
    url(r'^$', include('dateme_app.urls', namespace='dateme_app')),    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
