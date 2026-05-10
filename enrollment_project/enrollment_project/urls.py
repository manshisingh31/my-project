"""
URL configuration for enrollment_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls), 
#     path('', include('students.urls')), 
# ]
from django.contrib import admin
from django.urls import path
from students import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'), 
    path('users/', views.users, name='students_list'), 
    path('users/add/', views.add_student, name='add_student'),
    
    # Add this brand new line!
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('records/', views.records_list, name='records_list'),
    path('users/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('users/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('users/delete/<int:pk>/', views.delete_student, name='delete_student'), # <--- THIS LINE
    path('courses/edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('records/edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('records/closed/', views.closed_records, name='closed_records'),
]
