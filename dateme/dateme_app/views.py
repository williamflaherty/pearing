from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse

from dateme_app import controller
from dateme_app.serializers import *

# TODO: fix so it doesn't have to be csrf exempt

# HELPERS

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class Status(object):
    def __init__(self, success=False, data={}, exceptions=[], errors=[], status_code=403):
        self.success = success
        self.data = data
        self.exceptions = exceptions
        self.errors = errors
        self.status_code = status_code

    def serialize(self):
        temp = {}
        temp["success"] = self.success
        temp["data"] = self.data
        temp["exceptions"] = self.exceptions
        temp["errors"] = self.errors
        return temp

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'get_person': reverse('dateme_app:get_person', request=request, format=format),
        'register_person': reverse('dateme_app:register_person', request=request, format=format),
        'update_person': reverse('dateme_app:update_person', request=request, format=format)
    })

@csrf_exempt
def login(request, retval):

    """
    Authenticate a user and the API call. Can be used independently or as a helper method.
    """

    retval = Status(success=False, data={}, exceptions=["pre datas if"], errors=[], status_code=403)
    if (
        "person"   in request.DATA           and 
        "username" in request.DATA["person"] and
        "token"    in request.DATA["person"] and
        "app"      in request.DATA           and 
        "key"      in request.DATA["app"]
       ):

        # TODO: use person serializer with required fields?
        username = request.DATA["person"]["username"]
        token = request.DATA["person"]["token"]
        secret_key = request.DATA["app"]["key"]

        retval = Status(success=False, data={}, exceptions=["in datas if"], errors=[], status_code=403)
        if secret_key == "qahLbKqZG79E4N9XJV9nfdsj":

            retval = controller.authenticate_user(username, token, retval)
        else:
            retval.errors.append("010001")
    
    return retval

# GET
   
@csrf_exempt
@api_view(['POST'])
def get_person(request):

    """
    Get a user's general information. If the user does not exist, data will be null.  
    If more than one user with that username exists in the database, data will be null.  
    
    ### Response
    Object  

        {
            "data": 
            {
                "person": 
                {
                    "id": integer,
                    "username": string,
                    "handle": string,
                    "token": string,
                    "tagline": string,
                    "birthday": date,
                    "age_start": integer,
                    "age_end": integer,
                    "age": integer,
                    "gender": integer,
                    "orientation": integer
                    }
            }
            "errors": [<string>],
            "exceptions": [<string>],
            "success": boolean
        }

    Status codes  
    200: OK  
    403: Unauthorized  
    500: Unhandled exception  

    Error codes  
    0100: Unauthorized access to the Pearing API.  
    0101: This user failed Instagram's authorization.  
    0200: More than one user with this username in the database.  
    0201: The given username is already taken.  
    0202: The given username does not exist in the database.  

    ### Request object 

    Specification

        {
            "app":  
            {
                "key": string  
            },  
            "person":  
            {   
                "username": string,   
                "token": string   
            }  
        }  

    Example

        { 
            "app":  
            {  
                "key": "qahLbKqZG79E4N9XJV9nfdsj"  
            },  
            "person":  
            {   
                "username": "williamflaherty",  
                "token": "13863795.1fb234f.44d1de17b2cf43c098af6d3b3fd6735f"   
            }   
        }

    """

    retval = Status(success=False, data={}, exceptions=["not post"], errors=[], status_code=403)
    try:
        if request.method == 'POST':

            retval = login(request, retval)
            if retval.success:
                retval.status_code = 200
                username = request.DATA["person"]["username"]
                retval = controller.get_person(username, retval)
                if retval.success:
                    retval.data["person"] = (PersonSerializer(retval.data["person"])).data
    except Exception as e:
        retval.exceptions.append(str(e))
        retval.success = False
        retval.status_code = 500

    return JSONResponse(retval.serialize(), status=retval.status_code)

# INSERT/UPDATE

@csrf_exempt
@api_view(['POST'])
def register_person(request):
    
    """
    Register a new user along with their general information. The username must not already be in the database.

    ### Response
    Object  

        {
            "data": 
            {
                "person": 
                {
                    "id": integer,
                    "username": string,
                    "handle": string,
                    "token": string,
                    "tagline": string,
                    "birthday": date,
                    "age_start": integer,
                    "age_end": integer,
                    "age": integer,
                    "gender": integer,
                    "orientation": integer
                }
            }
            "errors": [<string>],
            "exceptions": [<string>],
            "success": boolean
        }

    Status codes  
    200: OK  
    403: Unauthorized  
    500: Unhandled exception  

    Error codes  
    0100: Unauthorized access to the Pearing API.  
    0101: This user failed Instagram's authorization.  
    0200: More than one user with this username in the database.  
    0201: The given username is already taken.  
    0202: The given username does not exist in the database.  

    ### Request object 

    Specification. Fields with asterisks `*` are optional.

        {
            "app":  
            {
                "key": string  
            },  
            "person": 
            {
                "id": integer,
                "username": string,
                "handle": string,
                "token": string,
                "tagline": string,*
                "birthday": date,
                "age_start": integer,
                "age_end": integer,
                "age": integer,
                "gender": integer,
                "orientation": integer
            }
        }

    Example

        { 
            "app": 
            {
                "key": "qahLbKqZG79E4N9XJV9nfdsj"
            },
            "person":
            {
                "username": "llmimimielll",
                "handle": "mischa",
                "token": "683953844.1fb234f.459a6f0519c147da9dd29dc53954d7b7",
                "birthday": "1991-10-09",
                "age_start": "20",
                "age_end": "25",
                "age": "23",
                "gender": 1,
                "orientation": 2
            } 
        }

    """

    retval = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)

    try:
        if request.method == 'POST':  

            retval = login(request, retval)
            if retval.success:    
                retval.status_code = 200
                person = PersonSerializer(data=request.DATA["person"])
                person_valid = person.is_valid()

                if person_valid:
                    person = person.create(person.validated_data)
                    retval = controller.register_person(person, retval)
                    if retval.success:
                        retval.data["person"] = (PersonSerializer(retval.data["person"])).data
                else:
                    retval.errors.extend(person.errors)
    except Exception as e:
        retval.exceptions.append(str(e))
        retval.success = False
        retval.status_code = 500

    return JSONResponse(retval.serialize(), status=retval.status_code)
   
@csrf_exempt
@api_view(['POST'])
def update_person(request):

    """
    Update a person's profile.

    ### Response
    Object  

        {
            "data": 
            {
                "person": 
                {
                    "id": integer,
                    "username": string,
                    "handle": string,
                    "token": string,
                    "tagline": string,
                    "birthday": date,
                    "age_start": integer,
                    "age_end": integer,
                    "age": integer,
                    "gender": integer,
                    "orientation": integer
                }
            }
            "errors": [<string>],
            "exceptions": [<string>],
            "success": boolean
        }

    Status codes  
    200: OK  
    403: Unauthorized  
    500: Unhandled exception  

    Error codes  
    0100: Unauthorized access to the Pearing API.  
    0101: This user failed Instagram's authorization.  
    0200: More than one user with this username in the database.  
    0201: The given username is already taken.  
    0202: The given username does not exist in the database.  

    ### Request object 

    Specification. Fields with asterisks `*` are optional.

        {
            "app":  
            {
                "key": string  
            },  
            "person": 
            {
                "id": integer,
                "username": string,
                "handle": string,
                "token": string,
                "tagline": string,*
                "birthday": date,
                "age_start": integer,
                "age_end": integer,
                "age": integer,
                "gender": integer,
                "orientation": integer
            }
        }

    Example

        { 
            "app": 
            {
                "key": "qahLbKqZG79E4N9XJV9nfdsj"
            },
            "person":
            {
                "username": "williamflaherty",  
                "handle": "willie",
                "token": "13863795.1fb234f.44d1de17b2cf43c098af6d3b3fd6735f", 
                "birthday": "1989-06-18",
                "age_start": "20",
                "age_end": "30",
                "age": "25",
                "gender": 2,
                "orientation": 1,
                "tagline": "Bridge. Chai Shai. Designing. Oh, and Boomer Sooner! I do what I want."
            } 
        }

    """
    # TODO: it shouldn't be a requirement to have all fields sans tagline as required.

    retval = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
   
    try:
        if request.method == 'POST': 

            is_auth = login(request, retval)
            if is_auth:

                retval.status_code = 200         
                person = PersonSerializer(data=request.DATA["person"])
                person_valid = person.is_valid()
                if person_valid:
                    person = person.create(person.validated_data)
                    retval = controller.update_person(person, retval)
                    if retval.success:
                        retval.data["person"] = (PersonSerializer(retval.data["person"])).data
                else:
                    retval.errors.extend(person.errors)

    except Exception as e:
        retval.exceptions.append(str(e))
        retval.success = False
        retval.status_code = 500

    return JSONResponse(retval.serialize(), status=retval.status_code)
 
# # NOT FIXED

# @csrf_exempt
# @api_view(['POST'])
# def get_messages(request):
#     retval = {
#         "success": False, 
#         "data": {}, 
#         "exception": "", 
#         "error": ""
#     }

#     if request.method == 'POST':
#         # TODO: authenticate the user via the token
#         user = models.Person.objects.get(username = request.DATA["user"]["username"]) 

#         # these are used for polling and limiting the number of messages, and are optional
#         num_messages = None     # all messages
#         last_time = 0           # from the beginning of time

#         if "last_time" in request.DATA:
#             last_time = request.DATA["last_time"]
        
#         if "num_messages" in request.DATA:
#             num_messages = request.DATA["num_messages"]
        
#         # request the last x messages from the last x time
#         retval = controller.get_messages(user, last_time, num_messages, retval) 

#         # serialize the data back into JSON
#         retval.data["messages"] = (MessageSerializer(retval.data["messages"])).data


#     # return data to Willie
#     return JSONResponse(retval, status=200)

# @csrf_exempt
# @api_view(['POST'])
# def add_message(request):
#     retval = {
#         "success": False, 
#         "data": {}, 
#         "exception": "", 
#         "error": ""
#     }

#     if request.method == 'POST':
#         # TODO: authenticate the user via the token
#         user = models.Person.objects.get(username = request.DATA["user"]["username"]) 

#         message = MessageSerializer(data=request.DATA["message"])
#         message_valid = message.is_valid()

#         if message_valid:
#             message = message.object
#             retval = controller.add_message(user, message, retval) 

#             # TODO: for now, am including the original info, but it may make sense to simply return T/F
#             retval.data["messages"] = (MessageSerializer(retval.data["messages"])).data
#             retval["success"] = True
#         else:
#             retval["error"] = message.errors
#     return JSONResponse(retval, status=200)

# @csrf_exempt
# @api_view(['POST'])
# def complete_challenge(request):
#     retval = {
#         "success": False, 
#         "data": {}, 
#         "exception": "", 
#         "error": ""
#     }

#     if request.method == 'POST':
#         # TODO: authenticate the user via the token
#         user = models.Person.objects.get(username = request.DATA["user"]["username"]) 

#         challenge = ChallengeSerializer(data=request.DATA["challenge"])
#         challenge_valid = challenge.is_valid()

#         if challenge_valid:
#             challenge = challenge.object
#             retval = controller.complete_challenge(user, challenge, retval) 
#         else:
#             retval["error"] = challenge.errors
#     return JSONResponse(retval, status=200)
    
# @csrf_exempt
# @api_view(['POST'])
# def match(request):
#     #JSON to recieve: {"user":{"username":"<user-to-receive-matches>"}}
#     retval = {
#         "success": False, 
#         "data": {}, 
#         "exception": "", 
#         "error": ""
#     }

#     if request.method == 'POST':
#         # TODO: authenticate the user via the token
        
#         #grab the username provided
#         username = request.DATA["user"]["username"]
        
#         #get the given user's person data
#         user = models.Person.objects.get(username__iexact=username)

#         #call match function
#         retval = controller.match(user, retval) 
        
#         #serialize data from the match function to be converted to JSON and handed back to app
#         retval.data["people"] = (PersonSerializer(retval.data["people"])).data
#     return JSONResponse(retval, status=200)

# @csrf_exempt
# @api_view(['POST'])
# def get_photos(request):
#     #JSON to recieve: {"user":{"username":"<user-to-receive-photos>"}}
#     retval = {
#         "success": False, 
#         "data": {}, 
#         "exception": "", 
#         "error": ""
#     }

#     if request.method == 'POST':
#         # TODO: authenticate the user via the token
#         user = models.Person.objects.get(username = request.DATA["user"]["username"]) 
        
#         # request photo urls from user
#         retval = controller.get_photos(user, retval) 

#         # serialize the data back into JSON
#         retval.data["photos"] = (PhotoSerializer(retval.data["photos"])).data

#     # return data to Willard
#     return JSONResponse(retval, status=200)

# @csrf_exempt
# @api_view(['POST'])
# def set_photos(request):
#     #JSON example: {"user":{"username":"doodman"}, "photos": [{"id": 1, "url": "http:\\\\i.imgur.com\\ZVfsM4A.jpg", "user": 1}, {"id": 2, "url": "http:\\\\i.imgur.com\\4K61Z1S.jpg", "user": 1}]}
#     retval = {
#         "success": False,
#         "error": ""
#     }
    
#     if request.method == 'POST':
#         user = models.Person.objects.get(username = request.DATA["user"]["username"])
        
#         photos = PhotoSerializer(data=request.DATA["photos"])
        
#         photos_valid = photos.is_valid()

#         if photos_valid:
#             retval = controller.set_photos(user, photos, retval)
#         else:
#             retval["error"] = photos.errors

#     return JSONResponse(retval, status=200)

# @csrf_exempt
# @api_view(['POST'])
# def get_location(request):
#     #JSON to recieve: {"user":{"username":"<user-to-retrieve-location-of>"}}
#     retval = {
#         "success": False, 
#         "data": {}, 
#         "exception": "", 
#         "error": ""
#     }

#     if request.method == 'POST':
#         # TODO: authenticate the user via the token
#         user = models.Person.objects.get(username = request.DATA["user"]["username"]) 
        
#         # request location from user
#         retval = controller.get_location(user, retval) 

#         # serialize the data back into JSON
#         retval.data["location"] = (LocationSerializer(retval.data["location"])).data

#     # return data to Willard
#     return JSONResponse(retval, status=200)

# @csrf_exempt
# @api_view(['POST'])
# def set_location(request):
#     #JSON example: {"user":{"username":"doodman"}, "location":{"user": 2, "latitude": "147.1489341", "longitude": "85.189034", "timestamp": "2014-01-08T21:55:31Z"}}
#     retval = {
#         "success": False,
#         "error": ""
#     }
    
#     if request.method == 'POST':
#         user = models.Person.objects.get(username = request.DATA["user"]["username"])
        
#         location = LocationSerializer(data=request.DATA["location"])
        
#         location_valid = location.is_valid()

#         if location_valid:
#             location = location.object
#             retval = controller.set_location(user, location, retval)
#         else:
#             retval["error"] = location.errors

#     return JSONResponse(retval, status=200)
