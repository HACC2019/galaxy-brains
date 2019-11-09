from django.shortcuts import render
from django.http import HttpResponse
import pyrebase

config = {
    'apiKey': "AIzaSyD4pquYNH5AnnnKTFmdRg0dzooWkwQrj8I",
    'authDomain': "scholar-system.firebaseapp.com",
    'databaseURL': "https://scholar-system.firebaseio.com",
    'storageBucket': "scholar-system.appspot.com",
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
firebase_auth = firebase.auth()
firebase_database = firebase.database()

def index(request):
    return render(request, 'index.html')
def createProject(request):
    return render(request, 'createproject.html')
def signup(request):
    return render(request, 'SignUp.html')

