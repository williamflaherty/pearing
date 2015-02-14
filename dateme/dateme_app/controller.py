import random
import urllib2
import json
#from datetime import date, datetime, time
import datetime
from dateme_app import models
from dateme_app.serializers import *
# TODO: why are serializers in here?
from django.utils import timezone

# NOTE: the general principle for now, is to let all the exceptions be caught by try/excepts in VIEWS.PY

# HELPERS

def authenticate_user_with_instagram(token):

    """
    Verify a user with the Instagram API
    """
    username = ""

    try:
        user_id = token.split(".", 1)[0]
        url = "https://api.instagram.com/v1/users/{0}?access_token={1}".format(user_id, token)
        f = urllib2.urlopen(url)
        response = json.loads(f.read())
        f.close()

        # check for existence of a username as indicator of success
        if "data" in response and "username" in response["data"]:
            username = response["data"]["username"]
    except Exception as e:
        # don't need to pass back any exceptions to the user
        # this is really the only time I feel compelled to swallow the exception so far, instead of letting it bubble up
        pass

    return username

# OTHER

def authenticate_user(user, token, status):

    """
    Authenticate new or existing users. A user's token is valid for 1 day after authentication.
    """
    # TODO: handle a user changing their username in instagram
    # TODO: trello - use https
    # example: https://api.instagram.com/v1/users/13863795?access_token=13863795.1fb234f.44d1de17b2cf43c098af6d3b3fd6735f

    status.success = False
    m = models.Person.objects.filter(username=user)
    
    # an existing user
    if len(m) == 1:
        
        m = m[0]
        
        # token not expired
        if m.token == token and m.token_expiration >= timezone.now():
            status.success = True
        # reauthenticate because token needs to be reauthenticated or token doesn't match what is stored
        else:
            username = authenticate_user_with_instagram(token)
            if username == user:
                # update the database if authentication with instagram was successful
                m.token = token
                m.token_expiration = timezone.now() + datetime.timedelta(days=1)
                m.save()
                status.success = True
            else:
                status.errors.append("010101")

    # a new person
    elif not m:
        username = authenticate_user_with_instagram(token)
        if username == user:
            status.success = True
        else:
            status.errors.append("010102")
    
    # somehow more than one person in the db
    else:
        status.errors.append("020001")

    return status

# GET
   
def get_person(user, status):

    """
    Get a user's general information.
    """
    status.success = False
    status.data["person"] = {}

    # get current person object from database
    m = models.Person.objects.filter(username=user)
    if len(m) == 1:
        # return person object and set success
        status.data["person"] = m[0]
        status.success = True
    elif m:
        status.errors.append("020002")
    else:
        status.errors.append("020202")

    return status

# INSERT/UPDATE

def register_person(person, status):
    
    """
    Register a new person with Pearing. The username can't already be taken.
    Authentication with Instagram should already have happened by this point,
    so save the token and set the expiration to be one day from now.
    """

    status.success = False
    status.data["person"] = {}

    m = models.Person.objects.filter(username=person.username)
    if m:
        status.errors.append("020101")
    else:
        p = models.Person(
            username = person.username, 
            handle = person.handle, 
            token = person.token, 
            token_expiration = timezone.now() + datetime.timedelta(days=1),
            tagline = person.tagline, 
            birthday = person.birthday, 
            age_start = person.age_start, 
            age_end = person.age_end, 
            gender = person.gender, 
            age = person.age_end,
            orientation = person.orientation
        )
        p.save()
        status.data["person"] = p
        status.success = True

    return status
    
def update_person(person, status):

    """
    Update a person's general information.
    """
    # TODO: make sure the token expiration is masked from the outside in all the return methods...

    status.success = False
    status.data["person"] = {}

    m = models.Person.objects.filter(username=person.username)
    if len(m) == 1:
        # update the person object in the database
        m = m[0]
        person.pk = m.pk
        person.token_expiration = m.token_expiration
        person.save()
        status.data["person"] = person
        status.success = True
    elif m:
        # more than one user found
        status.errors.append("020003")
    else:
        # no user found
        status.errors.append("020201")

    return status

def get_messages(user, status, last_time=None, num_messages=None):

    """
    Get a person's messages.
    """
    # TODO: should last_time variable

    # i think we should separate the status stuff from the backend logic and just handle
    # exceptions properly, but i'm just going to leave it as-is for now
    status = get_person(user, status)
    if status.success:
        status.success = False
        person = status.data["person"]
        messages = models.Message.objects.filter(sender=person).order_by('timestamp')
        
        if num_messages:
            messages = messages[:num_messages]
        status.data["messages"] = messages
        status.success = True

    # ugh. since we're passing status around we need to delete the person to avoid breaking the serializer
    # DC: do we want to include the person data in the response? i would think not, but i'm open to changing
    del status.data["person"]

    return status

# NOT FIXED

# # shamelessly stolen from http://stackoverflow.com/questions/2217488/age-from-birthdate-in-python/2259711#2259711
# def calculate_age(born):
#     born = born.date()
#     today = datetime.date.today()
#     try: 
#         birthday = born.replace(year=today.year)
#     except ValueError: # raised when birth date is February 29 and the current year is not a leap year
#         birthday = born.replace(year=today.year, day=born.day-1)
#     if birthday > today:
#         return today.year - born.year - 1
#     else:
#         return today.year - born.year

# def add_message(user, message, status):

#     # TODO: this needs a lot more work to handle the different content types
#     #       for now this should work for text

#     try:
#         status.success = False

#         # create the message object to be saved to database
#         m = models.Message(
#             contentType = models.ContentType.objects.get(pk=message.contentType.id),
#             sender = user,
#             value = message.value,
#             conversation = models.Conversation.objects.get(pk=message.conversation.id)
#         )

#         # if m.contentType.name is 'Challenge':
#         #     m.messagechallenge_set.create(
#         #         challenge=models.Challenge.objects.get(value=message.value),
#         #         isComplete=False
#         #     )

#             # mc.save()
        
#         # save message object to the database
#         m.save()
        
#         if m.contentType.name == "Challenge":
#             m.messagechallenge_set.create(
#                 challenge=models.Challenge.objects.get(value=message.value),
#                 isComplete=False
#             )

#         # assume it works and return success and the data we just saved
#         # it probably doesn't need to return the data we saved as it is just overhead...
#         status.data["messages"] = [m]
#         status.success = True

#     except Exception as e:
#         status["exception"] += str(e)
#         status["error"] += "\nThere was an issue."


#     return status

# def complete_challenge(user, challenge, status):

#     status.success = False

#     mc = models.MessageChallenge.objects.select_related('message__conversation').get(message__pk=challenge.message.pk, challenge__pk=challenge.challenge.pk, user=user)
#     challenge.pk = mc.pk
#     challenge.isComplete = True
#     challenge.save()

#     # update the level they are authorized for if they have completed all the ones at a level
#     # TODO: this should only work if all sides have completed the challenge
#     level_up = True
#     conversation_id = mc.message.conversation.pk
#     mcs = models.MessageChallenge.objects.filter(message__conversation__pk=conversation_id).values_list('challenge__pk', flat=True).order_by('challenge__pk')
#     challenges = models.Challenge.objects.filter(level=mc.message.conversation.level)
#     for challenge in challenges:
#         if challenge.pk not in mcs:
#             level_up = False

#     if level_up:
#         conversation = models.Conversation.objects.get(pk=conversation_id)
#         conversation.level += 1
#         conversation.save()

#     status.success = True

#     return status
    
# def match(user, status):

#     status.success = False
    
#     #calculate the birthdate ranges
#     old_date = datetime.date.today() - datetime.timedelta(days=user.age_end*365.24)
#     young_date = datetime.date.today() - datetime.timedelta(days=user.age_start*365.24)
#     your_age = calculate_age(user.birthday)

#     #calculate max and min lat/lon that we're willing to search for
#     # 1 degree of lat/lon is ~70 miles
#     loc = models.Location.objects.get(user=user)
#     min_lat = loc.latitude - 1
#     max_lat = loc.latitude + 1
#     min_lon = loc.longitude - 1
#     max_lon = loc.longitude + 1

#     # Retrieve users fitting criteria:
#     # Exclude yourself
#     people = models.Person.objects.exclude(username__iexact=user.username)
#     # Exclude users who are too young or too old
#     people = people.exclude(birthday__lte=old_date).exclude(birthday__gte=young_date)
#     # Exclude users who think YOU are too young or too old
#     people = people.exclude(age_start__gte=your_age).exclude(age_end__lte=your_age)
#     # Get users with appropriate orientation
#     people = people.filter(orientation__name__contains=user.gender.name).filter(gender__in=user.orientation.all())
#     # Get users within 1 degree of latitude/longitude
#     people = people.filter(location__latitude__gt=min_lat, location__latitude__lt=max_lat, location__longitude__gt=min_lon, location__longitude__lt=max_lon)
    
#     #If 5 or more people match the user's criteria, pick 5 random people; else, just pull the people who actually fit criteria
#     match_five = random.sample(people, min(5, people.count()))
#     print match_five
        
#     #setup data for return to JSON
#     status.success = True
#     status.data["people"] = match_five
#     print status
#     return status

# def get_photos(user, status):
    
#     status.success = False

#     # retrieve photos from user
#     # this should probably be ordered by time
#     photos = models.PhotoLink.objects.filter(user=user)
#     # photos = models.PhotoLink.objects.filter(user=user).order_by('timestamp')
    
#     status.data["photos"] = photos
#     status.success = True

#     return status

# def set_photos(user, photos, status):
    
#     status.success = False
    
#     # update the photo object in the database
#     # I can't figure out how to update multiple objects, so we'll just delete them for now
#     # and then save the new photos
#     m = models.PhotoLink.objects.filter(user=user).delete()
    
#     # save photo object to the database
#     photos.save()
    
#     # set success
#     status.success = True

#     return status

# def get_location(user, status):
    
#     status.success = False

#     # retrieve last location from user
#     location = models.Location.objects.filter(user=user)
    
#     status.data["location"] = location
#     status.success = True

#     return status

# def set_location(user, location, status):
    
#     status.success = False
    
#     # update the location object in the database or create new entry
#     m, created = models.Location.objects.get_or_create(user=user, defaults={'latitude':location.latitude,'longitude':location.longitude,'timestamp':location.timestamp})
    
#     if not created:
#         location.pk = m.pk
#         location.save()

#     # set success
#     status.success = True

#     return status
