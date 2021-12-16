"""cryptos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user import views as user_views
from django.contrib.auth import views as auth_views
from blog import views as blog_views
urlpatterns = [
    path('',user_views.home,name="home page"),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('blog/',include("blog.urls")),
    path('password-reset/',
    user_views.password_reset_request,name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password/password_reset_complete.html'), name='password_reset_complete'),     
]