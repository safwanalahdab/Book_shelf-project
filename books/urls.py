from django.urls import path , include 
from .views import * 
from . import views
from .views import * 
from rest_framework.routers import DefaultRouter 


router = DefaultRouter() 
router.register('', BookViewSet , basename = 'books' ) 

urlpatterns = [
       path('', views.book_page, name='book_page') ,
       path('api/', include( router.urls ) ) ,
]

