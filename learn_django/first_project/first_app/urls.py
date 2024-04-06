from django.urls import path
from first_app import views

urlpatterns = [
    path('hello/', views.my_hello_world),
    path('num/<int:num>/', views.print_num),
]