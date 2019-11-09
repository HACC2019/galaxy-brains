from django.shortcuts import render, redirect
from django.contrib import auth, messages
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

def signInSubmit(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        request.session['uid'] = str(user['idToken'])
    except:
        messages.success(request, ('Invalid Credentials'))
        return redirect('index')

    return redirect('landingPage')


def logoutSubmit(request):
    auth.logout(request)
    return render(request, 'index.html')

def landingPage(request):
    return render(request, 'landingPage.html')

def signUpSubmit(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    data = {'name': "Marty"}

    try:
        user = firebase_auth.create_user_with_email_and_password(email, password)
        results = firebase_database.child("users").child(user['localId']).set(data, user['idToken'])
        return redirect('index')
    except Exception as e:
        raise
