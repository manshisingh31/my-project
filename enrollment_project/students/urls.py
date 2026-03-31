from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('courses/', views.courses, name='courses'),
    path('enroll/', views.enroll, name='enroll'),
    path('records/', views.records, name='records'),
]