from rest_framework import serializers
from django.contrib.auth.models import User

class signupSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ('username','email')

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username',)
