from django.shortcuts import render
from rest_framework import viewsets, status 
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q , Count 
from books.models import Book , BorrowedBook , Category , Author 
from books.serializers import BookSerializers , BarrowBookSerilaizers , AuthorSerializers , CategorySerializers
from .serializers import UserAdminSeri 
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

# Create your views here.

User = get_user_model() 

class BookAdminView( viewsets.ModelViewSet ) : 
    queryset = Book.objects.all() 
    serializer_class = BookSerializers 
    permission_classes = [IsAdminUser] # just admin 

    def get_queryset ( self ) :
        #queryset = Book.objects.filter( is_archived = False )
        queryset = Book.objects.all().order_by("is_archived","-count_borrowed")
        author = self.request.query_params.get('author') 
        category = self.request.query_params.get('category') 

        if author : 
            queryset = queryset.filter( author__name__icontains = author ) 
        if category : 
            queryset = queryset.filter( category__name__icontains = category ) 
        
        return queryset 
    
    # archif 
    def destroy( self , request , *args , **kwargs ) : 
        book = self.get_object() 
        book.is_archived = True 
        book.is_avaiable = False 
        book.save() 
        return Response( { "Message" : "تمت الأرشفة بنجاح" } , status = status.HTTP_200_OK )
    
    @action( detail = True , methods = ['post'] , permission_classes = [IsAdminUser] ) 
    def restore( self , request , pk = None ) : 
        book = self.get_object() 

        if not book.is_archived :
            return Response({ "ERROR" : "الكتاب ليس مؤرشف "} , status = status.HTTP_400_BAD_REQUEST )
        
        book.is_archived = False 
        book.save() 
        return Response({"MESSAGE" : "تمت الغاء الارشفة بنجاح"} , status = status.HTTP_200_OK ) 
        
class UserAdminView( viewsets.ReadOnlyModelViewSet ) :
     serializer_class = UserAdminSeri 
     permission_classes = [IsAdminUser] 
     queryset = User.objects.all()
     
     def get_queryset(self) :
         return User.objects.annotate(
             borrowed_books_count = Count('borrower_book' , filter = Q( borrower_book__is_returned = False ))
         )
     

class BorrowedBookAdminViewSet( viewsets.ModelViewSet ) :
    serializer_class = BarrowBookSerilaizers
    permission_classes = [IsAdminUser] 
    queryset = BorrowedBook.objects.all() 

    def get_queryset( self ) :
        queryset = BorrowedBook.objects.filter( is_returned = False )
        return queryset 
    
    @action( detail = True , methods = ['post'] , permission_classes = [IsAdminUser] ) 
    def approve_return( self , request , pk = None ) : 
        borrow = self.get_object() 
        if not borrow.return_request : 
            return Response({"Erroe" : "المستخدم لم يقدم طلب استرجاع"} , status = status.HTTP_400_BAD_REQUEST )
        borrow.book.return_copy() 
        borrow.is_returned = True 
        borrow.return_date = borrow.return_request_date 
        borrow.save() 
        return Response({"MESSAGE" : "تمت استعادة الكتاب بنجاح"} , status = status.HTTP_200_OK )
    """
    @action( detail = True , methods = ['post'] , permission_classes = [IsAdminUser] ) 
    def reject_return( self , request , pk = None ) : 
        borrow = self.get_object() 
        if not borrow.return_request : 
            return Response({"Erroe" : "المستخدم لم يقدم طلب استرجاع"} , status = status.HTTP_400_BAD_REQUEST )
        return Response( {"MESSAGE" : "تم رفض طلب الاستعادة"} , status = status.HTTP_200_OK )
    """
class DashboardStatsView ( APIView ) :
    permission_classes = [IsAdminUser] 

    def get( self , request ) : 
        total_users = User.objects.count() 
        total_books = Book.objects.count() 
        borrowed_books = BorrowedBook.objects.filter( is_returned = False ).count()
        pending_returns = BorrowedBook.objects.filter( is_returned = False , return_request = True ).count()
        archived_books = Book.objects.filter( is_archived = True ).count() 
        available_books = Book.objects.filter( is_avaiable = True ).count() 

        data = {
             "total_users" : total_users , 
             "total_books" : total_books , 
             "borrowed_books" : borrowed_books , 
             "available_books" : available_books , 
             "pending_returns" : pending_returns , 
             "archived_books" : archived_books ,
            
        }
        return Response( data , status = status.HTTP_200_OK ) 
    
class CategoryAdminView( viewsets.ModelViewSet ) : 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializers 
    permission_classes = [IsAdminUser] 

class AuthorAdminView( viewsets.ModelViewSet ) : 
    queryset = Author.objects.all() 
    serializer_class = AuthorSerializers 
    permission_classes = [ IsAdminUser ] 
       