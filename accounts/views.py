from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import login 
from rest_framework import generics , status 
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny 
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework.decorators import api_view , permission_classes , authentication_classes 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count , Q 
from .serializers import * 

# Create your views here.
 
def account( request ) : 
    return HttpResponse('hello account') 

class RegisterView ( generics.CreateAPIView ) : 
    queryset = User.objects.all() 
    permission_classes = [ AllowAny ] 
    serializer_class = RegisterSerializer 

    def create( self , request , *args, **kwargs ) : 
        serilizer = self.get_serializer( data = request.data )
        serilizer.is_valid( raise_exception = True ) 

        user = serilizer.save() 

        token , created = Token.objects.get_or_create( user = user )

        login( request , user ) 

        data = {
            "message" : "تم انشاء المستخدم بنجاح " ,
            "user" : {
            "username" : user.username , 
            "email" : user.email , 
            "first_name" : user.first_name , 
            "last_name" : user.last_name ,
            }
            ,
            "token" : token.key 
        }

        return Response( data , status = status.HTTP_201_CREATED )
       
class LoginView ( ObtainAuthToken ) :
    permission_classes = [ AllowAny ] 
    authentication_classes = [ TokenAuthentication ] 

    def post( self, request, *args, **kwargs ) : 
         response =  super().post(request, *args, **kwargs) 
         if 'token' in response.data : 
          token = Token.objects.get( key = response.data['token'] )  
          data = {
            "message" : "تم تسجيل الدخول بنجاح " , 
            "status" : {
                "token" : token.key , 
                "user_id" : token.user.id ,
                "user_name" : token.user.username , 
            }
          }  
          return Response( data ) 
         
         return Response(
                {"error": "اسم المستخدم أو كلمة المرور غير صحيحة"},
                status= status.HTTP_400_BAD_REQUEST 
            )
    

class LogoutView( APIView ) : 

    def post( self , request ) : 
        request.user.auth_token.delete() 
        return Response({"message" : "تم تسجيل الخروج بنجاح "} , status = status.HTTP_200_OK  )
     

class ResetPasswordView( APIView ) :
    
    def post( self , request ) : 
        serilizaer = ResetPasswordSerilaizer( data = request.data , context =  { "request" : request } )
        serilizaer.is_valid( raise_exception = True ) 
        serilizaer.save() 
        return Response({"message" : "تم تغيير كلمة المرور بنجاح"} , status = status.HTTP_200_OK )  
    
class ProfileView( generics.RetrieveUpdateAPIView ) :
    serializer_class = ProfileSerializer

    def get_object( self ) :
        return User.objects.annotate( borrowed_books_count = Count( "borrower_book" , filter = Q( borrower_book__is_returned = False ) 
        )).get( id = self.request.user.id) 