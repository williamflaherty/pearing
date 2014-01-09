from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from dateme_app import controller
from dateme_app.serializers import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@api_view(['POST'])
def get_messages(request):
    retval = {
        "success": False, 
        "data": {}, 
        "exception": "", 
        "error": ""
    }

    if request.method == 'POST':
        # TODO: authenticate the user via the token
        user = models.Person.objects.get(username = request.DATA["user"]["username"]) 

        # these are used for polling and limiting the number of messages, and are optional
        num_messages = None     # all messages
        last_time = 0           # from the beginning of time

        if "last_time" in request.DATA:
            last_time = request.DATA["last_time"]
        
        if "num_messages" in request.DATA:
            num_messages = request.DATA["num_messages"]
        
        # request the last x messages from the last x time
        retval = controller.get_messages(user, last_time, num_messages, retval) 

        # serialize the data back into JSON
        retval["data"]["messages"] = (MessageSerializer(retval["data"]["messages"])).data


    # return data to Willie
    return JSONResponse(retval, status=200)

@csrf_exempt
@api_view(['POST'])
def add_message(request):
    retval = {
        "success": False, 
        "data": {}, 
        "exception": "", 
        "error": ""
    }

    if request.method == 'POST':
        # TODO: authenticate the user via the token
        user = models.Person.objects.get(username = request.DATA["user"]["username"]) 

        message = MessageSerializer(data=request.DATA["message"])
        message_valid = message.is_valid()

        if message_valid:
            message = message.object
            retval = controller.add_message(user, message, retval) 

            # TODO: for now, am including the original info, but it may make sense to simply return T/F
            retval["data"]["messages"] = (MessageSerializer(retval["data"]["messages"])).data
            retval["success"] = True
        else:
            retval["error"] = message.errors
    return JSONResponse(retval, status=200)

@csrf_exempt
@api_view(['POST'])
def save_person(request):
    #JSON example: {"user":{"username":"dcash"}, "person": {"id": 1, "username": "dcash", "handle": "dan", "token": "fake_token", "tagline": "cool guy", "birthday": "1990-06-11T21:44:12Z", "age_start": 20, "age_end": 50, "gender": 1, "orientation": [2]}}
    retval = {
        "success": False,
        "error": ""
    }
    
    if request.method == 'POST':
        user = models.Person.objects.get(username = request.DATA["user"]["username"])
        
        person = PersonSerializer(data=request.DATA["person"])
        
        person_valid = person.is_valid()

        if person_valid:
            person = person.object
            retval = controller.save_person(user, person, retval)
        else:
            retval["error"] = person.errors

    return JSONResponse(retval, status=200)
    
@csrf_exempt
@api_view(['POST'])
def get_person(request):
    retval = {
        "success": False,
        "data": {}
    }
    
    if request.method == 'POST':
        user = models.Person.objects.get(username = request.DATA["user"]["username"])
        
        retval = controller.get_person(user, retval)
        retval["data"]["person"] = (PersonSerializer(retval["data"]["person"])).data
        
    return JSONResponse(retval, status=200)

@csrf_exempt
@api_view(['POST'])
def complete_challenge(request):
    retval = {
        "success": False, 
        "data": {}, 
        "exception": "", 
        "error": ""
    }

    if request.method == 'POST':
        # TODO: authenticate the user via the token
        user = models.Person.objects.get(username = request.DATA["user"]["username"]) 

        challenge = ChallengeSerializer(data=request.DATA["challenge"])
        challenge_valid = challenge.is_valid()

        if challenge_valid:
            challenge = challenge.object
            retval = controller.complete_challenge(user, challenge, retval) 
        else:
            retval["error"] = challenge.errors
    return JSONResponse(retval, status=200)
    
@csrf_exempt
@api_view(['POST'])
def match(request):
    #JSON to recieve: {"user":{"username":"<user-to-receive-matches>"}}
    retval = {
        "success": False, 
        "data": {}, 
        "exception": "", 
        "error": ""
    }

    if request.method == 'POST':
        # TODO: authenticate the user via the token
        
        #grab the username provided
        username = request.DATA["user"]["username"]
        
        #get the given user's person data
        user = models.Person.objects.get(username__iexact=username)

        #call match function
        retval = controller.match(user, retval) 
        
        #serialize data from the match function to be converted to JSON and handed back to app
        retval["data"]["people"] = (PersonSerializer(retval["data"]["people"])).data
    return JSONResponse(retval, status=200)

@csrf_exempt
@api_view(['POST'])
def get_photos(request):
    #JSON to recieve: {"user":{"username":"<user-to-receive-photos>"}}
    retval = {
        "success": False, 
        "data": {}, 
        "exception": "", 
        "error": ""
    }

    if request.method == 'POST':
        # TODO: authenticate the user via the token
        user = models.Person.objects.get(username = request.DATA["user"]["username"]) 
        
        # request photo urls from user
        retval = controller.get_photos(user, retval) 

        # serialize the data back into JSON
        retval["data"]["photos"] = (PhotoSerializer(retval["data"]["photos"])).data

    # return data to Willard
    return JSONResponse(retval, status=200)

@csrf_exempt
@api_view(['POST'])
def set_photos(request):
    #JSON example: {"user":{"username":"doodman"}, "photos": [{"id": 1, "url": "http:\\\\i.imgur.com\\ZVfsM4A.jpg", "user": 1}, {"id": 2, "url": "http:\\\\i.imgur.com\\4K61Z1S.jpg", "user": 1}]}
    retval = {
        "success": False,
        "error": ""
    }
    
    if request.method == 'POST':
        user = models.Person.objects.get(username = request.DATA["user"]["username"])
        
        photos = PhotoSerializer(data=request.DATA["photos"])
        
        photos_valid = photos.is_valid()

        if photos_valid:
            retval = controller.set_photos(user, photos, retval)
        else:
            retval["error"] = photos.errors

    return JSONResponse(retval, status=200)

@csrf_exempt
@api_view(['POST'])
def get_location(request):
    #JSON to recieve: {"user":{"username":"<user-to-retrieve-location-of>"}}
    retval = {
        "success": False, 
        "data": {}, 
        "exception": "", 
        "error": ""
    }

    if request.method == 'POST':
        # TODO: authenticate the user via the token
        user = models.Person.objects.get(username = request.DATA["user"]["username"]) 
        
        # request location from user
        retval = controller.get_location(user, retval) 

        # serialize the data back into JSON
        retval["data"]["location"] = (LocationSerializer(retval["data"]["location"])).data

    # return data to Willard
    return JSONResponse(retval, status=200)

@csrf_exempt
@api_view(['POST'])
def set_location(request):
    #JSON example: {"user":{"username":"doodman"}, "location":{"user": 2, "latitude": "147.1489341", "longitude": "85.189034", "timestamp": "2014-01-08T21:55:31Z"}}
    retval = {
        "success": False,
        "error": ""
    }
    
    if request.method == 'POST':
        user = models.Person.objects.get(username = request.DATA["user"]["username"])
        
        location = LocationSerializer(data=request.DATA["location"])
        
        location_valid = location.is_valid()

        if location_valid:
            location = location.object
            retval = controller.set_location(user, location, retval)
        else:
            retval["error"] = location.errors

    return JSONResponse(retval, status=200)