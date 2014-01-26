from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Gender(models.Model):
    name = models.CharField(max_length = 20, unique = True)
    
    def __unicode__(self):
        return self.name

# TODO: do we need registration statuses?
class Person(models.Model):
    username = models.CharField(max_length = 100)
    handle = models.CharField(max_length = 35)
    token = models.CharField(max_length = 200)
    token_expiration = models.DateTimeField()
    tagline = models.CharField(max_length = 300, blank = True)
    birthday = models.DateField()
    age_start = models.IntegerField()
    age_end = models.IntegerField()
    gender = models.ForeignKey(Gender, related_name='gender')
    orientation = models.ForeignKey(Gender, related_name='orientation')
    # orientation = models.ManyToManyField(Gender, related_name='orientation')
    age = models.IntegerField()
    # TODO: add bisexuality back in later
    def __unicode__(self):
        return self.username

class Setting(models.Model):
    user = models.ForeignKey(Person) 
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
    level = models.IntegerField()
    # first_person = models.ForeignKey(Person, related_name='first_person')
    # second_person = models.ForeignKey(Person, related_name='second_person')
    people = models.ManyToManyField(Person)

class Message(models.Model):
    contentType = models.ForeignKey(ContentType)
    conversation = models.ForeignKey(Conversation)
    sender = models.ForeignKey(Person)
    # receiver = models.ForeignKey(User, related_name='receiver')
    timestamp = models.DateTimeField(auto_now = True)
    value = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.contentType.name, self.value)

class Challenge(models.Model):
    title = models.CharField(max_length = 100, unique = True)
    value = models.CharField(max_length = 255, unique = True)
    level = models.IntegerField()

    def __unicode__(self):
        return u'%s: %s' % (self.title, self.value)


class Location(models.Model):
    user = models.ForeignKey(Person)
    latitude = models.DecimalField(max_digits = 13, decimal_places = 10)
    longitude = models.DecimalField(max_digits = 13, decimal_places = 10)
    timestamp = models.DateTimeField()

class MessageChallenge(models.Model):
    # TODO: picture probably shouldn't be a text field
    challenge = models.ForeignKey(Challenge)
    message = models.ForeignKey(Message)
    picture = models.TextField(blank = True)
    user = models.ForeignKey(Person)
    isComplete = models.BooleanField()

    # TODO: this should be included but I'm tired and having a hard time with the serializer
    # class Meta:
    #     unique_together = ('challenge', 'message')

    def __unicode__(self):
        return u'%s' % (self.message)

class PhotoLink(models.Model):
    url = models.CharField(max_length = 128)
    user = models.ForeignKey(Person)

    # TODO: timestamp probably needed
    #timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.url
