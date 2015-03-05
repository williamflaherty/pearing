from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from dateme_app import models

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    
    """
    A ModelSerializer that takes additional 'fields' and 'exclude' arguments 
    that control which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields', 'exclude' args up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the 'fields' argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude:
            # Drop any fields that are specified in the 'exclude' argument.
            not_allowed = set(exclude)
            existing = set(self.fields.keys())
            for field_name in (existing & not_allowed):
                self.fields.pop(field_name)

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Setting
        fields = ('name', 'value')
    
class ContentTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ContentType
        fields = ('id', 'name')

class PersonSerializer(DynamicFieldsModelSerializer):
    
    # TODO: include settings

    def create(self, validated_data):
        return models.Person(**validated_data)

    class Meta:
        model = models.Person
        exclude = ['token_expiration']

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Message
        fields = ('id', 'conversation', 'sender', 'timestamp', 'value', 'contentType')

class ChallengeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.MessageChallenge
        fields = ('id', 'challenge', 'message', 'picture', 'isComplete', 'user')

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PhotoLink
        fields = ('id', 'url', 'user')
        #fields = ('id', 'url', 'user', 'timestamp')

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = ('id', 'user', 'latitude', 'longitude', 'timestamp')

