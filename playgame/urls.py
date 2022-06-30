from django.contrib import admin
from django.urls import path
from playgame import views

urlpatterns = [
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('register/',views.registeruser,name='register'),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name= "room"),
    path('createroom/',views.createroom,name='createroom'),
    path('updateroom/<str:pk>/',views.updateroom,name='updateroom'),
    path('deleteroom/<str:pk>/',views.deleteroom,name='deleteroom'),
    path('deletemessage/<str:pk>/',views.deletemessage,name='deletemessage'),
    path('profile/<str:pk>/',views.userprofile,name='userprofile'),
    path('course',views.showcourses,name='back'),
    path('coursed/<int:courses_id>/',views.details,name='details'),
    path('adk/',views.vp,name='adk'),
    
]