from django.urls import path
from . import views
from .views import ContactAPI

urlpatterns = [
    path('contact/', ContactAPI.as_view(), name='contact'),
]
