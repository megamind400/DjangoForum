from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="homepage"),
    path('room/<str:pk>/', views.room, name="room"),

    path("loginReg/", views.loginreg, name="loginreg"),
    path("create-room/", views.CreateRoom, name="create-room"),
    path("upate-room/<str:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),

]