"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.urls import path
from . import views
from .views import (
    UserAPI, LoginAPI,
    ForgotPasswordAPI, VerifyOTPAPI, ResetPasswordAPI
)

urlpatterns = [
    path('', UserAPI.as_view(), name='root'),
    path('user/', views.UserAPI.as_view(), name='user_api'),
    path('<int:id>/', UserAPI.as_view(), name='_detail'), 

    path('login/', LoginAPI.as_view(), name='login'),
    path('register/', views.UserAPI.as_view(), name='user_api'),
    
    path('forgot-password/', ForgotPasswordAPI.as_view()),
    path('verify-otp/', VerifyOTPAPI.as_view()),
    path('reset-password/', ResetPasswordAPI.as_view()),
]

