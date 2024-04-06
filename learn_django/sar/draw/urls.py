from django.urls import path
from draw import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    #name is for template referencing
]
app_name='draw'#for namespacing