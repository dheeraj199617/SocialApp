from django.urls import path 
from .import views 

urlpatterns = [

    path('signup/',views.SignUpView.as_view()),
    
    path("login/",views.LoginView.as_view()),

    path('fetch-my-profile/',views.FetchMyProfile.as_view()),

    path('logout/',views.LogOutView.as_view())

]