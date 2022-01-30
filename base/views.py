from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import re
from django import http
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room



def home(request):
    roomsvar = Room.objects.all()    
    context = {'rooms': roomsvar}
    return render(request, 'base/home.html', context)   

def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room': room}
    return render(request, 'base/room.html',context )    


def CreateRoom(request):
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    context = {'form': form}
    print("im here")
    return render(request, 'base/room_form.html', context)