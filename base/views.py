from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import re
from django import http
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import context

from .forms import RoomForm
from .models import Room,Topic



def home(request):

    q = request.GET.get('search') if request.GET.get('search') != None else ''
    #print(q)
    roomsvar = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topic = Topic.objects.all()
    roomcount = roomsvar.count()
    context = {'rooms': roomsvar, 'topic': topic, 'room_count': roomcount}
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


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('homepage')
    return render(request, 'base/delete.html',{'obj':room})