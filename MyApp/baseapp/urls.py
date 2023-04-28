from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userlogin, name='login'),
    path('register/', views.registeruser, name='register'),
    path('logout/', views.userlogout, name='logout'),
    path('', views.home, name='Home'),
    path('room/<str:pk>', views.room, name='Room'),
    path('create/', views.create, name='create'),
    path('update/<str:pk>', views.update, name='update'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('delete-message/<str:pk>', views.delete_message, name='delete-message'),
    path('profile/<str:pk>', views.userprofile, name='userprofile'),

]
