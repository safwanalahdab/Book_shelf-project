from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model() 


class UserAdminSeri( serializers.ModelSerializer ) :
    borrowed_books_count = serializers.IntegerField(read_only=True)
    class Meta : 
        model = User 
        fields = ['id','username','email','first_name','last_name','borrowed_books_count']
        read_only_fields = ['borrowed_books_count']
        

