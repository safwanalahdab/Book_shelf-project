from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Author, Book, BorrowedBook, Category
from books.serializers import (
    AuthorSerializers,
    BarrowBookSerilaizers,
    BookSerializers,
    CategorySerializers,
)
from .serializers import UserAdminSeri


User = get_user_model() 

class BookAdminView( viewsets.ModelViewSet ) : 
    queryset = Book.objects.all() 
    serializer_class = BookSerializers 
    permission_classes = [IsAdminUser] # just admin 

    def get_queryset ( self ) :
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

"""
###BookAdminView

### GET /dashboard/books/

**Description**  
Returns a list of all books (both archived and active) for administrative purposes. Results are ordered by archive status and popularity.

**Permissions**  
- `IsAdminUser` – only admin users can access this endpoint.

**Ordering**  
- First by `is_archived` (non-archived books first).
- Then by `-count_borrowed` (most borrowed books first).

**Query Parameters**
- `author` *(optional, string)*  
  Filters books by author name (case-insensitive, partial match).  
  Example: `?author=Naguib`
- `category` *(optional, string)*  
  Filters books by category name (case-insensitive, partial match).  
  Example: `?category=Novel`

**Response (200 OK)**  
Returns a list of `BookSerializers` objects.

"""

class UserAdminView( viewsets.ReadOnlyModelViewSet ) :
     serializer_class = UserAdminSeri 
     permission_classes = [IsAdminUser] 
     queryset = User.objects.all()
     
     def get_queryset(self) :
         return User.objects.annotate(
             borrowed_books_count = Count('borrower_book' , filter = Q( borrower_book__is_returned = False ))
         )
     
"""
### UserAdminView
### GET /admin/users/

**Description**  
Returns a read-only list of all users in the system, annotated with the number of books each 
user is currently borrowing (i.e., not yet returned).

**Permissions**  
- `IsAdminUser` – only admin users are allowed to access this endpoint.

**Behavior**  
Each user object is annotated with:
- `borrowed_books_count`: the number of `BorrowedBook` records linked to this user where `is_returned = False`.

This is implemented using:
- `annotate(borrowed_books_count=Count('borrower_book', filter=Q(borrower_book__is_returned=False)))`

**Response (200 OK)**  
Returns a list of `UserAdminSeri` objects. A typical response item may look like:
"""

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
### BorrowedBookAdminViewSet
### GET /dashboard/borrowed-books/

**Description**  
Returns a list of all *active* borrowed-book records (i.e., borrowings that have not yet been marked as returned).

**Permissions**  
- `IsAdminUser` – only admin users can access this endpoint.

**Behavior**  
The queryset is restricted to:
- `BorrowedBook.objects.filter(is_returned=False)`

So only currently borrowed (open) records are included.

**Response (200 OK)**  
Returns a list of `BarrowBookSerilaizers` objects.

"""

class DashboardStatsView ( APIView ) :
    permission_classes = [IsAdminUser] 

    def get( self , request ) : 
        total_users = User.objects.count() 
        total_books = Book.objects.count() 
        today = timezone.localdate()
        start = today - timedelta(days = 6 )  
        borrowed_books = BorrowedBook.objects.filter( is_returned = False ).count()
        pending_returns = BorrowedBook.objects.filter( is_returned = False , return_request = True ).count()
        archived_books = Book.objects.filter( is_archived = True ).count() 
        available_books = Book.objects.filter( is_avaiable = True ).count() 
        category_stats = (
           Category.objects.annotate(
               books_count = Count('category')
           )
           .values('id','name','books_count')
        )
        history = (
            BorrowedBook.objects.filter( borrow_date__range = ( start , today ) ) 
            .values("borrow_date") 
            .annotate( count = Count("id")) 
        )

        counts_map = {row["borrow_date"]: row["count"] for row in history }
        borrowed_last_7_days = [
            {
              "date": (start + timedelta(days=i)).strftime("%Y %m %d"),  
              "count": counts_map.get(start + timedelta(days=i), 0),
            }
            for i in range(7)
        ]

        data = {
             "total_users" : total_users , 
             "total_books" : total_books , 
             "borrowed_books" : borrowed_books , 
             "available_books" : available_books , 
             "pending_returns" : pending_returns , 
             "archived_books" : archived_books ,
             'category_stats' : category_stats ,
             'borrowed_last_7_days' : borrowed_last_7_days ,
            
        }
        return Response( data , status = status.HTTP_200_OK ) 


"""
### DashboardStatsView
### GET /dashboard/stats/

**Description**  
Provides a summary of key statistics for the admin dashboard, including counts of users, books, borrowing activity, category breakdown, and borrow history for the last 7 days.

**Permissions**  
- `IsAdminUser` – only admin users can access this endpoint.

**Response (200 OK)**  

"""

class CategoryAdminView( viewsets.ModelViewSet ) : 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializers 
    permission_classes = [IsAdminUser] 


"""

### CategoryAdminView
### PUT /dashboard/categories/{id}/
### PATCH /dashboard/categories/{id}/

**Description**  
Updates an existing category (full update with PUT, partial update with PATCH).

**Permissions**  
- `IsAdminUser`

---

### DELETE /dashboard/categories/{id}/

**Description**  
Deletes a category.

**Permissions**  
- `IsAdminUser`

**Response (204 No Content)**  
Category successfully deleted.

"""

class AuthorAdminView( viewsets.ModelViewSet ) : 
    queryset = Author.objects.all() 
    serializer_class = AuthorSerializers 
    permission_classes = [ IsAdminUser ] 


"""
### AuthorAdminView

Admin CRUD API for managing authors.

"""