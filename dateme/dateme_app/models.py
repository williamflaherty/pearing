from django.db import models
from django.contrib.auth.models import User

# TODO: do we need registration statuses?
class Person(models.Model):
    user = models.OneToOneField(User)
    isValidated = models.BooleanField()
    tagline = models.CharField(max_length = 300, blank = True)

    def __unicode__(self):
        return self.user.username

class Setting(models.Model):
    user = models.ForeignKey(User) 
    name = models.CharField(max_length = 255)
    value = models.CharField(max_length = 255)
    
    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

class ContentType(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    
    def __unicode__(self):
        return self.name

class Conversation(models.Model):
    subscriber = models.ForeignKey(User)

class Message(models.Model):
    contentType = models.ForeignKey(ContentType)
    conversation = models.ForeignKey(Conversation)
    sender = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now = True)
    value = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.contentType.name, self.value)