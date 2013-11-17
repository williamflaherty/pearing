from django.conf.urls import patterns, url
from dateme_app import views

urlpatterns = patterns('',
    # url(r'^home/$', views.home, name='home'),
    url(r'^add_message/$', views.add_message, name='add_message'),
    url(r'^get_messages/$', views.get_messages, name='get_messages'),
	url(r'^save_fields/$', views.save_fields, name='save_fields'),
	url(r'^get_fields/$', views.get_fields, name='get_fields'),
	url(r'^complete_challenge/$', views.complete_challenge, name='complete_challenge'),
)
