from django.contrib import admin
from dateme_app.models import *

admin.site.register(Message)
admin.site.register(ContentType)
admin.site.register(Conversation)
admin.site.register(Person)
admin.site.register(Setting)

