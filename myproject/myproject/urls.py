from django.db import models



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

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("customer/", include('customer.urls')),  # This includes your app's URL configuration

# ]




from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Define a view for the root path to return a welcome message or a default response
def home(request):
    return HttpResponse("Welcome to the Customer API! Use /customer/ to interact with the API.")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),  # Admin URL
    path('customer/', include('customer.urls')),  # Your app's customer URLs
    path('user/', include('user.urls')), 
    path('plan/', include('plan.urls')), 
    path('transaction/', include('transaction.urls')), 
    path('deposite/', include('deposite.urls')),
    path('expense/', include('expense.urls')), # This is the root path '/' that returns a welcome message
]
