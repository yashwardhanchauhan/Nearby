from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from . import models
from rest_framework.views import APIView
from . import serializers
from django.contrib.auth.models import User,auth
import requests

# Create your views here.
class SignUp(generics.CreateAPIView):
    serializer_class = serializers.signupSerializer
    queryset =User.objects.all()

class Login(APIView):
    def post(self,request):
        try:
            email_id=request.POST.get("email_id")
            password=request.POST.get("password")
            qs=User.objects.filter(email=email_id,password=password).distinct()
            serializer=serializers.LoginSerializer(qs,many=True)
            if serializer is not None:
                response={'status': status.HTTP_200_OK,'message':'Login successfull','data':serializer.data }
            else:
                response = {'status': status.HTTP_204_NO_CONTENT,'message':'Email Id and Password doesnt match','data':serializer.data }
            return Response(response, status=response['status'])
        except:
            response = {'status': status.HTTP_400_BAD_REQUEST ,'message':'Bad Request'}
            return Response(response, status=response['status'])


#Using MyIndiaMap API
token='bece0337-a537-4a03-b32a-16a2c91b5bab'
class Search(APIView):
    def get(self,request):
        try:
            keyword=request.GET.get("keywords")
            refLocation=request.GET.get("refLocation")
            response=requests.get("https://atlas.mapmyindia.com/api/places/nearby/json?keywords={}&refLocation={}".format(keyword,refLocation), headers={'Authorization': 'Bearer {}'.format(token)})
            data=response.json()
            if response.status_code==200:
                response={'status': status.HTTP_200_OK,'message':'Search successfull','data':data }
            else:
                response = {'status': status.HTTP_204_NO_CONTENT,'message':'Invalid Search No Content Available','data':data }
            return Response(response, status=response['status'])
        except:
            response = {'status': status.HTTP_400_BAD_REQUEST ,'message':'Bad Request'}
            return Response(response, status=response['status'])
            

