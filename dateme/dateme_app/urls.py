from django.conf.urls import patterns, url
from dateme_app import views

urlpatterns = patterns('',
    
    # OTHER
    url(r'^login/$', views.login, name='login'),

    # GET
    url(r'^get_person/$', views.get_person, name='get_person'),

    # INSERT/UPDATE
    url(r'^register_person/$', views.register_person, name='register_person'),
	url(r'^update_person/$', views.update_person, name='update_person'),

    # NOT FIXED
 #    url(r'^add_message/$', views.add_message, name='add_message'),
 #    url(r'^get_messages/$', views.get_messages, name='get_messages'),
 #    url(r'^complete_challenge/$', views.complete_challenge, name='complete_challenge'),
 #    url(r'^match/$', views.match, name='match'),
 #    url(r'^get_photos/$', views.get_photos, name='get_photos'),
 #    url(r'^set_photos/$', views.set_photos, name='set_photos'),
 #    url(r'^get_location/$', views.get_location, name='get_location'),
 #    url(r'^set_location/$', views.set_location, name='set_location'),
)
