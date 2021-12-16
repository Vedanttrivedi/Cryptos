from django.urls import path
from . import views

urlpatterns = [
    path('',views.blogList,name="blogListPage"),
    
]