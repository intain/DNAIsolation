from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.home, name='user-home'),
    path('register', user_views.register, name='user-register'),
    path('login', auth_views.LoginView.as_view(template_name='UserHandling/login.html'), name='user-login'),
    path('logout', auth_views.LogoutView.as_view(template_name='UserHandling/logout.html'), name='user-logout')
]
