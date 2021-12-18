from django.urls import path
from . import views

urlpatterns = [
    path('',views.blogList,name="blogListPage"),
    path('create/',views.blogCreate,name="blogCreatePage"),
    path('<int:id>/',views.oneBlog,name="oneBlogPage"),
    path('comment/',views.comment,name="commentPage"),
]