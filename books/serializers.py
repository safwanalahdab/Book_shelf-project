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
    image = serializers.ImageField( use_url = True , allow_null = True , required=False) 
    
    author_id = serializers.PrimaryKeyRelatedField(
        source='author',              # يربطه بحقل author في الموديل
        queryset=Author.objects.all(),
        write_only=True,
        required=False,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',            # يربطه بحقل category في الموديل
        queryset=Category.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    class Meta : 
        model = Book 
        fields = ['id','title','author','author_id','image','category','category_id','description','possition','total_copies','available_copies','count_borrowed','is_avaiable','is_archived','pages','publication_year' , 'isbn' ]  
        read_only_fields = ["id"] 

class BarrowBookSerilaizers ( serializers.ModelSerializer ) : 
     book = BookSerializers( read_only = True ) 
     borrower = serializers.StringRelatedField( read_only = True )

     #due_date = serializers.SerializerMethodField()
     #late_day = serializers.SerializerMethodField()

     class Meta : 
         model = BorrowedBook 
         fields = ['id','book','borrower','borrow_date','return_request','return_date','is_returned','notes','due_date','late_day','return_request_date']
    
"""
     def get_due_date(self, obj):
        return obj.due_date
        
        Called by DRF when serializing the 'due_date' field.

        It simply returns the value of the model property 'due_date'.

     def get_late_day(self, obj):
        return obj.late_day 
"""
