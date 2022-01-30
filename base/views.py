from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from django import http
from django.http import HttpResponse
from django.shortcuts import render

from .models import Room



def home(request):
    roomsvar = Room.objects.all()    
    context = {'rooms': roomsvar}
    return render(request, 'base/home.html', context)   

def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room': room}
    return render(request, 'base/room.html',context )    
