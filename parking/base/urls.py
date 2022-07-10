from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homeDemo'),
    path('test/home', views.home, name='home'),
    path('user/', views.user, name='user'),
    path('test/update', views.adminPage, name='adminPage'),
    path('test/update/slotUpdate', views.slotUpdater, name='admin'),
    path('test/book', views.bookSlot, name='bookSlot'),
    path('save/', views.saveImage, name='save'),
]
