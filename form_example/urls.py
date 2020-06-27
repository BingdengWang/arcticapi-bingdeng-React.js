from api import views
from django.urls import path
from form_example import views

urlpatterns = [
    path('myform/', views.myform),
]
