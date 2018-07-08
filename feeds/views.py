from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def feeds(request):
    pass


def sources(request):
    if request.method == 'GET':
        return HttpResponse(request, 'Hello world')
