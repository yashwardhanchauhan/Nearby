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
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import  formatdate
import smtplib

# Create your views here.
class SignUp(generics.CreateAPIView):
    serializer_class = serializers.signupSerializer
    queryset =User.objects.all()

class Login(APIView):
    def post(self,request):
        try:
            email_id=request.POST.get("email_id")
            password=request.POST.get("password")
            qs=User.objects.filter(email=email_id,password=password)
            serializer=serializers.LoginSerializer(qs,many=True)
            if len(qs)!=0:
                response={'status': status.HTTP_200_OK,'message':'Login successfull','data':serializer.data }
            else:
                response = {'status': status.HTTP_204_NO_CONTENT,'message':'Email Id and Password doesnt match' }
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
            
def send_mail(send_to, subject, text):
    send_from = 'sender mail'
    #assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))


    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(send_from, "senders mail password")
    text = msg.as_string()
    server.sendmail(send_from, send_to, text)
    server.quit()

from random import randint

class Signup_with_mail(APIView):
    def post(self,request):
        try:
            email_id=request.POST.get("email_id")
            password=request.POST.get("password")
            
            if User.objects.filter(email=email_id).exists()==False:
                user=User(email=email_id,password=password)
                user.save()
                send_to = email_id
                code=randint(100000, 999999)
                subject = 'Registration for the Nearby application ' 
                text = 'Verification Code for the mail is:' + str(code)
                send_mail(send_to,subject,text)
                response={'status': status.HTTP_200_OK,'message':'Code Has been send to your mail','Code':code }
            else:
                response = {'status': status.HTTP_204_NO_CONTENT,'message':'Email Id Already Exists' }
            return Response(response, status=response['status'])
        except:
            response = {'status': status.HTTP_400_BAD_REQUEST ,'message':'Bad Request'}
            return Response(response, status=response['status'])
