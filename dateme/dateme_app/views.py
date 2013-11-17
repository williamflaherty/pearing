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
    retval = {
        "success": False,
        "error": ""
    }
    
    if request.method == 'POST':
        user = models.Person.objects.get(username = request.DATA["user"]["username"])
        
        person = PersonSerializer(data=request.DATA["person"])
        
        person_valid = person.is_valid()

        if person_valid:
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
    retval = {
        "success": False, 
        "data": {}, 
        "exception": "", 
        "error": ""
    }

    if request.method == 'POST':
        # TODO: authenticate the user via the token
        user = models.Person.objects.get(username = request.DATA["user"]["username"]) 

        retval = controller.match(user, retval) 
    return JSONResponse(retval, status=200)


