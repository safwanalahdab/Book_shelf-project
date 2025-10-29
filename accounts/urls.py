from django.urls import path 
from . import views 
from .views import * 


urlpatterns = [
      path('', views.account, name='account') , 
      path('register' , RegisterView.as_view() , name = "register" ) ,
      path('login' , LoginView.as_view() , name = "login" ) ,
      path('logout' , LogoutView.as_view() , name = "logout" ) ,
      path('change_password' , ResetPasswordView.as_view() , name = "change_password" ) ,
      path('profile' , ProfileView.as_view() , name = "profile" ) ,

]


