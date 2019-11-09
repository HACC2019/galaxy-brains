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
    messages.success(request, ('You have been logged out'))

    return render(request, 'index.html')

def landingPage(request):
    return render(request, 'landingPage.html')

def projectPage(request):
    return render(request, 'project_page.html')

def createProjectSubmit(request):
    data = {
            "description": request.POST.get('description'),
            "sweat": request.POST.get('sweat'),
            "timeframe": request.POST.get('timeframe')
            # Need to add breath-standards as well
            }
    gradeLevel = request.POST.get('gradeLevel')

    if gradeLevel == 'k' or gradeLevel <= 5:
        school = "elementary"
    elif gradLevel <= 8:
        school = "middle"
    else:
        school = "high"

    firebase_database.child("projects").child("potential-projects").child(school).child(gradeLevel).(request.POST.get('projectName')).set(data)   

    return redirect('landingPage')
