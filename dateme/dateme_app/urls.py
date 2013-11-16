from django.conf.urls import patterns, url
from dateme_app import views

urlpatterns = patterns('',
    # url(r'^home/$', views.home, name='home'),
    url(r'^add_message/$', views.add_message, name='add_message'),
    url(r'^get_messages/$', views.get_messages, name='get_messages'),
)
