from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import re
from django import http
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import context
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.test import RequestFactory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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

@login_required(login_url='loginreg') #if the user is not logged in redirect to 'loginreg'
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

@login_required(login_url='loginreg') #if the user is not logged in redirect to 'loginreg'
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #instance prefills the text boxes with previous information

    if request.user != room.host: #chekcing if user is authenticated to edit
        messages.error(request, 'you dont have the required permissions to edit this room')
        return redirect('homepage')

    if request.method == 'POST': #edit method
        form = RoomForm(request.POST, instance=room) #instance updates the room instead of creating a new one
        if form.is_valid():
            form.save()
            return redirect('homepage')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='loginreg') #if the user is not logged in redirect to 'loginreg'
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.error(request, 'you dont have the required permissions to delete this room')
        return redirect('homepage')
    if request.method == 'POST':
        room.delete()
        return redirect('homepage')
    return render(request, 'base/delete.html',{'obj':room})

@login_required(login_url='loginreg') #if the user is not logged in, redirect to 'loginreg'
def logoutuser(request):
    logout(request)
    return redirect('homepage')

def registerpage(request):
    form = UserCreationForm()
    print('before post check')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'an error occurred during registration, please read the requirements carefully or use another username')    
    return render(request, 'base/LoginReg.html',{'regform':form})

def loginreg(request):
    pagename = 'login'
    if request.user.is_authenticated:
        logout(request)    
        return redirect('login')
    if request.method == 'POST':
        usernamevar = request.POST.get('username').lower()
        passwordvar = request.POST.get('password')
        print("username:", usernamevar)
        try:
            user = User.objects.get(username=usernamevar)

        except:
            messages.error(request, 'wrong Username or Password') 

        user = authenticate(request, username=usernamevar, password=passwordvar)
        if user is not None:
            login(request, user)
            return redirect('homepage')

    context = {'pagename': pagename}
    return render(request, 'base/LoginReg.html', context)