from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="homepage"),
    path('room/<str:pk>/', views.room, name="room"),

    path("logoutuser/", views.logoutuser, name="logout-user"),
    path("loginReg/", views.loginreg, name="loginreg"),
    path("create-room/", views.CreateRoom, name="create-room"),
    path("upate-room/<str:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),
    path("register/", views.registerpage, name="register-user"),

]