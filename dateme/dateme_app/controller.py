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

    try:
        status["success"] = False

        # create the message object to be saved to database
        m = models.Message(
            contentType = models.ContentType.objects.get(pk=message.contentType.id),
            sender = user,
            value = message.value,
            conversation = models.Conversation.objects.get(pk=message.conversation.id)
        )

        # if m.contentType.name is 'Challenge':
        #     m.messagechallenge_set.create(
        #         challenge=models.Challenge.objects.get(value=message.value),
        #         isComplete=False
        #     )

            # mc.save()
        
        # save message object to the database
        m.save()
        
        if m.contentType.name == "Challenge":
            m.messagechallenge_set.create(
                challenge=models.Challenge.objects.get(value=message.value),
                isComplete=False
            )

        # assume it works and return success and the data we just saved
        # it probably doesn't need to return the data we saved as it is just overhead...
        status["data"]["messages"] = [m]
        status["success"] = True

    except Exception as e:
        status["exception"] += str(e)
        status["error"] += "\nThere was an issue."


    return status

def save_fields(user, person, status):
    
    status["success"] = False
    
    # update the person object in the database
    m = models.Person.objects.get(user)
    person.pk = m.pk
    
    # save person object to the database
    person.save()
    
    # set success
    status["success"] = True

    return status
    
def get_fields(user, status):

    # get current person object from database
    m = models.Person.objects.get(user)
    
    # return person object and set success
    status["data"]["Person"] = m
    status["success"] = True

    return status

def complete_challenge(user, challenge, status):

    status["success"] = False

    mc = models.MessageChallenge.get(message__pk=challenge.message, challenge__pk=challenge.challenge.pk)
    challenge.pk = mc.pk
    challenge.isComplete = True
    challenge.save()
    status["success"] = True

    return status
