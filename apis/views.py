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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import datetime
from django.utils.timezone import utc
from rest_auth.views import LogoutView
from random import randint


# Create your views here.
class SignUp(generics.CreateAPIView):
    serializer_class = serializers.signupSerializer
    queryset =User.objects.all()

class Login(ObtainAuthToken):
    def post(self,request):
        # try:
        email_id=request.POST.get("email_id")
        password=request.POST.get("password")
        qs=User.objects.filter(email=email_id,password=password)
        serializer=serializers.LoginSerializer(qs,many=True)
        if len(qs)!=0:
            token,created=Token.objects.get_or_create(user=User.objects.get(email=email_id,password=password))
            if not created:
                created = datetime.datetime.utcnow()
                token.save()
            response={'status': status.HTTP_200_OK,'message':'Login successfull','data':serializer.data,'token':token.key }
        else:
            response = {'status': status.HTTP_204_NO_CONTENT,'message':'Email Id and Password doesnt match' }
        return Response(response, status=response['status'])
        # except:
        #     response = {'status': status.HTTP_400_BAD_REQUEST ,'message':'Bad Request'}
        #     return Response(response, status=response['status'])

class Logout(LogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        request.user.auth_token.delete()
        response={'message':"Logout successfully"}
        return Response(response,status=status.HTTP_200_OK)


        


#Using MyIndiaMap API

def readingtoken():
    s=''
    with open("C:/Users/admin/projects/nearbyapis/apis/token.txt","r") as f:
        s=f.read()
    return s

def modifyingtoken():
    f=open("C:/Users/admin/projects/nearbyapis/apis/token.txt","w")
    url = "https://outpost.mapmyindia.com/api/security/oauth/token"
    grant_type = 'client_credentials'
    client_id = "33OkryzDZsIuJ-q-hQx_kUD73j7vP4zSXxjRb6eE7QDNJpRA7Qphpiq_2708Ho5iG-2AB08ZOJCT7UChLF0ZuK_pQaxfOzPseXGMV6U-6sYAq6YYDA-JCQ=="
    client_secret = "lrFxI-iSEg_bPOrlEssw54i0mzky1a5ofL-yZgrAvcvfnDscuTAhLxndgfpL6Uj5FNM4jXoNQwwl3k-mkZDjKCJcy3La870YTVDV98bGAa-3J0MtEoaIK3UMhhSIoO6G"
    myobj = {'grant_type': grant_type,
        'client_id' : client_id,
        'client_secret' : client_secret
        }
    x = requests.post(url, data = myobj).json()
    f.write(x['access_token'])
    f.close()
    return x['access_token']


class Search(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # try:
        token=readingtoken()
        keyword=request.GET.get("keywords")
        refLocation=request.GET.get("refLocation")
        response=requests.get("https://atlas.mapmyindia.com/api/places/nearby/json?keywords={}&refLocation={}".format(keyword,refLocation), headers={'Authorization': 'Bearer {}'.format(token)})
    
        data=response.json()
        print(data)
        if 'error'in data.keys() and data["error"]=="invalid_token":
            token=modifyingtoken()
            response=requests.get("https://atlas.mapmyindia.com/api/places/nearby/json?keywords={}&refLocation={}".format(keyword,refLocation), headers={'Authorization': 'Bearer {}'.format(token)})
            data=response.json()
            
        dataslist = {}
        for i in range(10):
            xdistance = str(data["suggestedLocations"][i]['distance'])
            xlatitude = str(data["suggestedLocations"][i]['latitude'])
            xlongitude = str(data["suggestedLocations"][i]['longitude'])
            xplacename = data["suggestedLocations"][i]['placeName']
            xplaceaddress=data["suggestedLocations"][i]['placeAddress']
            xdata = [xdistance,xlatitude,xlongitude,xplacename,xplaceaddress]
            dataslist[i] = xdata
            #print(dataslist)
        if response.status_code==200:
            response={'status': status.HTTP_200_OK,'message':'Search successfull','data':dataslist }
        else:
            response = {'status': status.HTTP_204_NO_CONTENT,'message':'Invalid Search No Content Available','data':data }
        return Response(response, status=response['status'])
        # except:
        #     response = {'status': status.HTTP_400_BAD_REQUEST ,'message':'Bad Request'}
        #     return Response(response, status=response['status'])
            
def send_mail(send_to, subject, text):
    send_from = ''#Email


    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))


    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(send_from, "")#password
    text = msg.as_string()
    server.sendmail(send_from, send_to, text)
    server.quit()



# class Signup_with_mail(APIView):
#     def post(self,request):
#         #try:
#         username=request.POST.get("username")
#         email_id=request.POST.get("email_id")
#         password=request.POST.get("password")
#         if User.objects.filter(username=username).exists()==False:   
#             if  User.objects.filter(email=email_id).exists()==False:
#                 user=User(username=username,email=email_id,password=password)
#                 token = Token.objects.create(user=user)
#                 send_to = email_id
#                 code=randint(100000, 999999)
#                 subject = 'Registration for the Nearby application ' 
#                 text = 'Hey'+str(username)+'Verification Code for the mail is:' + str(code)
#                 send_mail(send_to,subject,text)
#                 response={'status': status.HTTP_200_OK,'message':'Code Has been send to your mail','Code':code,'Token':token.key }
#                 user.save()
#             else:
#                 response = {'status': status.HTTP_204_NO_CONTENT,'message':'Email Id Already Exists' }
#             return Response(response, status=response['status'])
#         else:
#                 response = {'status': status.HTTP_204_NO_CONTENT,'message':'Username Already Exists' }
#                 return Response(response, status=response['status'])
        
        # except:
        #     response = {'status': status.HTTP_400_BAD_REQUEST ,'message':'Bad Request'}
        #     return Response(response, status=response['status'])


class Send_mail(APIView):
    def post(self,request):
        send_to = request.POST.get('email_id')
        code=randint(100000, 999999)
        subject = 'Your One Time Password [{}]'.format(str(code)) 
        text = str(code)
        send_mail(send_to,subject,text)
        response={'status': status.HTTP_200_OK,'message':'Code Has been send to your mail'}
        return Response(response, status=response['status'])

class DeleteAccount(APIView):
    def POST(self,request):
        try:
            user = request.POST.get('username')
            user=User.objects.get(username=user)
            user.delete()
            return Response({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist: 
            return Response({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND) 

class AllUsers(APIView):
    def get(self,request):
        qs=User.objects.all()
        serializer=serializers.AllUsersSerializer(qs,many=True)
        if len(serializer.data) != 0:
            response = {'status': status.HTTP_200_OK,'message':'success','data':serializer.data }
        else:
            response = {'status': status.HTTP_204_NO_CONTENT,'message':'No Content','data':serializer.data }
        return Response(response, status=response['status'])