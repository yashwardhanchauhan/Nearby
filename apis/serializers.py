from rest_framework import serializers
from . import models
from django.contrib.auth.models import User,auth
class signupSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ("email","username")
