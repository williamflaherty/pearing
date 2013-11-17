from django.db import models

class Gender(models.Model):
    name = models.CharField(max_length = 20, unique = True)

# TODO: do we need registration statuses?
class Person(models.Model):
    username = models.CharField(max_length = 100, unique = True)
    handle = models.CharField(max_length = 35, unique = True)
    token = models.CharField(max_length = 200)
    tagline = models.CharField(max_length = 300, blank = True)
    birthday = models.DateTimeField()
    age_start = models.IntegerField()
    age_end = models.IntegerField()
    gender = models.ForeignKey(Gender, related_name='gender')
    orientation = models.ManyToManyField(Gender, related_name='orientation')

    def __unicode__(self):
        return self.user.username

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
    sender = models.ForeignKey(User, related_name='sender')
    # receiver = models.ForeignKey(User, related_name='receiver')
    timestamp = models.DateTimeField(auto_now = True)
    value = models.TextField()

    def __unicode__(self):
        return u'%s: %s' % (self.contentType.name, self.value)

class Challenge(models.Model):
    title = models.CharField(max_length = 100, unique = True)
    value = models.CharField(max_length = 255, unique = True)
    level = models.IntegerField()








