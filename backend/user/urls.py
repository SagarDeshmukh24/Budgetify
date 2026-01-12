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
from .views import UserAPI, LoginAPI, forgot_password, reset_password, verify_otp
from . import views

urlpatterns = [
    path('', UserAPI.as_view(), name='root'),
    path('user/', views.UserAPI.as_view(), name='user_api'),
    path('<int:id>/', UserAPI.as_view(), name='_detail'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('register/', views.UserAPI.as_view(), name='user_api'),
    path('forgot_password/',forgot_password, name='forgot_password'),
    path('reset-password/',reset_password, name='reset-password'),
    path('verify_otp/',verify_otp, name='verify_otp'),



# wrong =>
    # path('', views.get, name='CustomerAPI'),
    # path("customer", views.get, name="customer"),
    # path("", views.get, name="customer"),
]
