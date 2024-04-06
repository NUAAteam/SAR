from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def my_hello_world(request):
    return HttpResponse("Hello World!")
def print_num(request, num):
    if num%2==0:
      s="even"
    else:
      s="odd"
    return HttpResponse(f"{num} is {s}")