from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseNotFound, Http404
import pyrebase
import json

config = {
    'apiKey': "AIzaSyD4pquYNH5AnnnKTFmdRg0dzooWkwQrj8I",
    'authDomain': "scholar-system.firebaseapp.com",
    'databaseURL': "https://scholar-system.firebaseio.com",
    'storageBucket': "scholar-system.appspot.com",
}

firebase = pyrebase.initialize_app(config)
metadata = {"loggedin": False}

"""
raise Http404
"""
# Get a reference to the auth service
firebase_auth = firebase.auth()
firebase_database = firebase.database()

def index(request):
    global metadata
    print(metadata["loggedin"])
    if metadata["loggedin"]:
        return render(request, 'landingPage.html', metadata)
    else:
        return render(request, 'index.html', metadata)

def signup(request):
    if metadata["loggedin"]:
        return redirect('404')
    else:
        return render(request, 'signup.html', metadata)

def signInSubmit(request):
    global metadata
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        request.session['uid'] = str(user['idToken'])
        metadata["loggedin"] = True
    except:
        messages.success(request, ('Invalid Credentials'))
        return redirect('index')
    return redirect('index')

def signUpSubmit(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    firstName = request.POST.get('firstName')
    lastName = request.POST.get('lastName')
    role = request.POST.get('role')

    data = {'firstName': firstName,
            'lastName': lastName,
            'role': role,
            'email': email
    }

    try:
        user = firebase_auth.create_user_with_email_and_password(email, password)
        results = firebase_database.child("users").child(user['localId']).set(data, user['idToken'])
    except Exception as e:
        messages.success(request, json.loads(e.args[1])['error']['message'])
        return redirect('index')
        
    return redirect('index')


def logoutSubmit(request):
    global metadata
    metadata["loggedin"] = False
    auth.logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('index')

def landingPage(request):
    global metadata
    print(f"landingPage: {metadata['loggedin']}")
    return render(request, 'landingPage.html', metadata)

def projectPage(request):
    return render(request, 'project_page.html', metadata)

def createproject(request):
    if metadata["loggedin"]:
        return render(request, 'createproject.html', metadata)
    else:
        return redirect('404')

def projectPage(request, project = ""):
    projectdict = getProjectFromName(project)
    return render(request, 'project_page.html', projectdict)

def pageNotFound(request):
    return render(request, '404.html')

def createProjectSubmit(request):
    data = {
            "description": request.POST.get('description'),
            "sweat": request.POST.get('sweat'),
            "timeframe": request.POST.get('timeframe')
            # Need to add breath-standards as well as tags
            }
    gradeLevel = request.POST.get('gradeLevel')

    if gradeLevel == 'k' or gradeLevel <= 5:
        school = "elementary"
    elif gradeLevel <= 8:
        school = "middle"
    else:
        school = "high"

    firebase_database.child("projects").child("potential-projects").child(school).child(gradeLevel).child(request.POST.get('projectName')).set(data)

    return redirect('landingPage')

def getProjectFromName(name):
    try:
        result = firebase_database.child("projects").child("approved-projects").child(name).get().val()
    except:
        try:
            result = firebase_database.child("projects").child("potential-projects").child(name).get().val()
        except:
            result = None

    return result
