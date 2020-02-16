from rest_framework import serializers

from core.models import Emplyee,Event
from django.contrib.auth.models import User,Group

class EmpyeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emplyee
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
from django.contrib.auth.models import User, Group
# from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="core:user-detail")
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']