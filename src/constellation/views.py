from django.shortcuts import render, redirect
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

def signInSubmit(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    print(email)
    print(password)

    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
    except:
        return redirect('placeholder')

    return render(request, 'landingPage.html')
