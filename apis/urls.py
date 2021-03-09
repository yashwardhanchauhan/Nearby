from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/',views.SignUp.as_view()),
    path('login/',views.Login.as_view()),
    path('search/',views.Search.as_view()),
    #path('signup_with_mail/',views.Signup_with_mail.as_view()),
    path('Logoutall/',views.Logout.as_view()),
    path('sendmail/',views.Send_mail.as_view()),
    path('delete_account/',views.DeleteAccount.as_view()),
    path('all_users/',views.AllUsers.as_view()),
]