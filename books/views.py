from django.shortcuts import render 
from django.http import HttpResponse 
from rest_framework import viewsets , status 
from rest_framework.decorators import action 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import responses , Response
from .models import Book , BorrowedBook 
from .serializers import * 
from rest_framework.decorators import api_view , permission_classes 
from rest_framework.permissions import AllowAny 

# Create your views here.


def book_page( request ) :
    return HttpResponse("hadialabrash1111") 


class BookViewSet( viewsets.ReadOnlyModelViewSet ) :
    
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    permission_classes = [ AllowAny ]     
    def get_queryset( self ) :
      queryset = Book.objects.all()
      author = self.request.query_params.get('author') 
      category = self.request.query_params.get('category') 

      if author :
         queryset = queryset.filter( author__name__icontains = author ) 
      if category : 
         queryset = queryset.filter( category__name__icontains = category ) 

      return queryset 
      
      
    @action( detail = True , methods = ['post'] , permission_classes = [IsAuthenticated] ) 
    def borrow( self , request , pk = None ) : 
         book = self.get_object() 
         user = request.user 

         if not book.borrow_book() :
            return Response({"error" : "الكتاب غير متاح حاليا"} , status = status.HTTP_400_BAD_REQUEST )
         
         BorrowedBook.objects.create( book = book , borrower = user ) 
         return Response({"success" : "تمت الاستعارة بنجاح"} , status = status.HTTP_201_CREATED ) 
         

          
        
