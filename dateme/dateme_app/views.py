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
    	# authenticate the user
        # user = authenticate(username=sender.object.username, password=sender.object.password)
        user = authenticate(username=request.DATA["user"]["username"], password=request.DATA["user"]["password"])
         
        # these are used for polling and limiting the number of messages, and are optional
        num_messages = None		# all messages
        last_time = 0			# from the beginning of time

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
        user = authenticate(username=request.DATA["user"]["username"], password=request.DATA["user"]["password"])
        #request.DATA["message"]["sender"] = user.pk
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
