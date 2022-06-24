"""management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from core.views import HomeView, DashboardView,register_request,login_request,profile, createGroup, getGroups,delGroups, join, leave, ForgetPassword,ChangePassword
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView),
    path('signup/', register_request,name="register"),
    path('group/add', createGroup, name="createGroup"),
    path('group/', getGroups, name="getGroups"),
    path('group/del/<str:name>/', delGroups, name="delGroups"),
    path('group/join/<str:name>', join, name='join'),
    path('group/leave/<str:name>', leave, name='leave'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("logout", auth_views.LogoutView.as_view(template_name='accounts\logout.html'), name="logout"),
    path('accounts/profile/', profile, name='profile'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),
]
