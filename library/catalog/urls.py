from django.urls import path
from django.http import HttpResponse

def placeholder(request):
    return HttpResponse("Catalog app pronta")

urlpatterns = [
    path('', placeholder, name='index'),
]