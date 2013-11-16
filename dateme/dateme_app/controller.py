from django.contrib.auth.models import User
from datetime import date, datetime, time
from dateme_app import models
from dateme_app.serializers import *

def get_messages(user, lastTime, num_messages, status):

    # TODO: should lastTime variable
    
    status["success"] = False
    messages = models.Message.objects.filter(sender=user).order_by('timestamp')
    if num_messages:
        messages = messages[:num_messages]
    status["data"]["messages"] = messages
    status["success"] = True

    return status

def add_message(user, message, status):

    # TODO: this needs a lot more work to handle the different content types
    #       for now this should work for text

    status["success"] = False

    # create the message object to be saved to database
    m = models.Message(
        contentType = models.ContentType.objects.get(pk=message.contentType.id),
        sender = user,
        value = message.value,
        conversation = models.Conversation.objects.get(pk=message.conversation.id)
    )
    
    # save message object to the database
    m.save()

    # TODO: how to know if save was successful?
    #   if m.pk maybe?
    #   or a try/catch?

    # assume it works and return success and the data we just saved
    # it probably doesn't need to return the data we saved as it is just overhead...
    status["data"]["messages"] = [m]
    status["success"] = True

    return status
