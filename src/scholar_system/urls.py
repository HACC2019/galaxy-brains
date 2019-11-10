"""scholar_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from constellation import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('signInSubmit/', views.signInSubmit),
    path('landingPage/', views.landingPage, name='landingPage'),
<<<<<<< HEAD
    path('signup', views.signup, name='signup'),
    path('logoutSubmit', views.logoutSubmit, name='logoutSubmit'),
    path('createProject', views.createProject, name='createProject'),
=======
>>>>>>> Initialized project page
    path('signup', views.signup, name='signup'),
    path('projectPage/', views.projectPage, name='projectPage'),
    path('createproject/', views.createproject, name='createproject')
]
