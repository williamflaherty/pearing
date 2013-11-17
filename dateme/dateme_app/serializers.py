from django.contrib.auth.models import User
from rest_framework import serializers
from dateme_app import models

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Setting
        fields = ('name', 'value')
		
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('id', 'user', 'isValidated', 'tagline')

class UserSerializer(DynamicFieldsModelSerializer):
    setting_set = SettingSerializer(many=True, required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'setting_set')
    
class ContentTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.ContentType
        fields = ('id', 'name')

class PersonSerializer(serializers.ModelSerializer):
    
    # TODO: include settings

    class Meta:
        model = models.Person
        fields = ('id', 'username', 'handle', 'token', 'tagline', 'birthday', 'age_start', 'age_end', 'gender', 'orientation')

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Message
        fields = ('id', 'conversation', 'sender', 'timestamp', 'value', 'contentType')
