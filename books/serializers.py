"""
serializers to convert from frontend to JSON 

"""

from rest_framework import serializers 
from django.contrib.auth import get_user_model 
from .models import Category , Book , Author , BorrowedBook 

user = get_user_model() 

class AuthorSerializers ( serializers.ModelSerializer ) :

    class Meta : 
        model = Author
        fields = "__all__" 

class CategorySerializers (serializers.ModelSerializer ) : 

    class Meta : 
        model = Category 
        fields = "__all__" 

class BookSerializers ( serializers.ModelSerializer ) :
    author = AuthorSerializers( read_only = True ) 
    category = CategorySerializers( read_only = True , allow_null=True ) 
    image = serializers.ImageField( use_url = True , allow_null = True ) 

    class Meta : 
        model = Book 
        fields = ['id','title','author','image','category','description','possition','total_copies','is_avaiable']  

class BarrowBookSerilaizers ( serializers.ModelSerializer ) : 
     book = BookSerializers( read_only = True ) 
     borrower = serializers.StringRelatedField( read_only = True )

     class Meta : 
         model = BorrowedBook 
         fieldes = ['id','book','borrower','borrow_date','return_date','is_returned','notes']



