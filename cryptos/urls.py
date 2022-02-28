from django.contrib import admin
from django.urls import path,include
from user import views as user_views
from django.contrib.auth import views as auth_views
from blog import views as blog_views
from Currency import views as cu_views
from prediction import views as pd_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',user_views.home,name="home page"),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('converter/',cu_views.converter,name="currency converter"),
    path('news/',cu_views.getNews,name="mainnews"),
    path("coinnews/<currency>",cu_views.currencyNews,name="currencyNews"),
    path('session/',cu_views.printSession,name="session values"),
    path('user/',include('user.urls')),
    path('blog/',include("blog.urls")),
    path('prediction/',pd_views.predict,name="prediction"),
    path('discussion/',include("Discussion.urls")),
    path('password-reset/',
    user_views.password_reset_request,name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password/password_reset_complete.html'), name='password_reset_complete'),     
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)