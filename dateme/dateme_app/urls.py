from django.conf.urls import patterns, url
from dateme_app import views

urlpatterns = patterns('',
    # url(r'^home/$', views.home, name='home'),
    url(r'^add_message/$', views.add_message, name='add_message'),
    url(r'^get_messages/$', views.get_messages, name='get_messages'),
	url(r'^save_person/$', views.save_person, name='save_person'),
	url(r'^get_person/$', views.get_person, name='get_person'),
	url(r'^complete_challenge/$', views.complete_challenge, name='complete_challenge'),
)
