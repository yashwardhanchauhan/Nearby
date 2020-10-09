from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/',views.SignUp.as_view()),
    path('login/',views.Login.as_view()),
    path('search/',views.Search.as_view()),
]