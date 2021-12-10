from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login,name="loginPage"),
    path('register/',views.register,name="registerPage")
]

