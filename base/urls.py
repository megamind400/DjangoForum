from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="homepage"),
    path('room/<str:pk>/', views.room, name="room"),

]