from django.urls import path
from . import views

urlpatterns = [

    path('createview/',views.create,name='create'),
    path('',views.listBook,name='index'),
    path('detailsview/<int:book_id>/',views.detailsview,name='detail'),
    path('updateview/<int:book_id>/',views.updatebook,name='update'),
    path('deleteview/<int:book_id>/',views.deleteview,name='delete'),
    path('author/',views.createAuthor,name='author'),
    path('search/',views.search_book,name='search'),
    
    
]