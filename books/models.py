from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Author ( models.Model ) :
    name = models.CharField( max_length = 100 ) 
    
    def __str__( self ) :
        return self.name 
    
class Category ( models.Model ) :
    name = models.CharField( max_length = 100 ) 
    
    def __str__( self ) :
      return self.name


class Book ( models.Model ) : 
    title = models.CharField( max_length = 100 ) 
    description = models.CharField( max_length = 1000 )
    image = models.ImageField( upload_to = 'books/' , null = True , blank = True )
    author = models.ForeignKey( Author , on_delete = models.SET_NULL , related_name = 'author' , null = True ) 
    category = models.ForeignKey( Category , on_delete = models.SET_NULL , related_name = 'category' , null = True ) 
    total_copies = models.PositiveIntegerField( default = 1 ) 
    created_at = models.DateTimeField( auto_now_add = True )
    is_avaiable = models.BooleanField( default = True ) 
    possition = models.CharField( max_length = 10 , null = True ) 
    is_archived = models.BooleanField( default = False ) 
    
    """
    this function to boorow 
    """
    def borrow_book( self ) :
        if self.total_copies == 0 :
            return False 
        self.total_copies -= 1 
        self.is_avaiable = self.total_copies > 0 
        self.save( update_fields = [ 'total_copies' , 'is_avaiable' ] )
        return True 
    
    """
    this function to return coppy 
    """

    def return_copy( self ) :
        self.total_copies += 1 
        self.total_copies = True 
        self.save( update_fields = [ 'total_copies' , 'total_copies' ] ) 

    def __str__( self ) : 
        return self.title 
    
class BorrowedBook ( models.Model ) :
     book = models.ForeignKey( Book , on_delete = models.CASCADE , related_name = "borrowed_book" ) 
     borrower = models.ForeignKey( User , on_delete = models.CASCADE , related_name = "borrower_book") 
     borrow_date = models.DateField( auto_now_add = True ) 
     return_date = models.DateField( blank = True , null = True )
     is_returned = models.BooleanField( default = False ) 
     notes = models.TextField( blank = True , null = True , default = "" )  
     return_request = models.BooleanField( default = False ) 

     def __str__( self ) : 
         return self.book.title 
     

