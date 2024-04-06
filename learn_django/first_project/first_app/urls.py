from django.urls import path
from first_app import views

urlpatterns = [
    path('hello/', views.my_hello_world, name='hello'),
    path('num/<int:num>/', views.print_num,name='num'),
    #name is for template referencing
]
app_name='first_app'#for namespacing