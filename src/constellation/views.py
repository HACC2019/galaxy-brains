from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseNotFound, Http404
import pyrebase
import json
import re

config = {
    'apiKey': "AIzaSyD4pquYNH5AnnnKTFmdRg0dzooWkwQrj8I",
    'authDomain': "scholar-system.firebaseapp.com",
    'databaseURL': "https://scholar-system.firebaseio.com",
    'storageBucket': "scholar-system.appspot.com",
}

firebase = pyrebase.initialize_app(config)

"""
raise Http404
"""
# Get a reference to the auth service
firebase_auth = firebase.auth()
firebase_database = firebase.database()

def index(request):
    try:
        user = firebase_auth.get_account_info(request.session['uid'])['users'][0]['localId']
        request.session['metadata'] = {'loggedin': True, 'role': firebase_database.child('users').child(user).child('role').get(request.session['uid']).val()}
        request.session['metadata']['recentschools'] = recentProjectsSchools(3)
        return render(request, 'landingPage.html', request.session['metadata'])
    except:
        request.session['metadata'] = {'loggedin': False}
        return render(request, 'index.html', request.session['metadata'])

def signup(request):
    try:
        firebase_auth.get_account_info(request.session['uid'])
        return redirect('404')
    except:
        return render(request, 'signup.html', request.session['metadata'])

def signInSubmit(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        request.session['uid'] = str(user['idToken'])
    except:
        messages.success(request, ('Invalid Credentials'))

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


def logoutSubmit(request):
    auth.logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('index')

def landingPage(request):
    return render(request, 'landingPage.html', request.session['metadata'])

def projectListCard(request):
    return render(request, 'projectlistcard.html', request.session['metadata'])

def createproject(request):
    try:
        localId = firebase_auth.get_account_info(request.session['uid'])['users'][0]['localId']
    except:
        return redirect('index')

    if firebase_database.child("users").child(localId).child('role').get(request.session['uid']).val() == 'teacher':
        return render(request, 'createproject.html', request.session['metadata'])
    else:
        return redirect('404')

def projectPage(request, project = ""):
    request.session['metadata']["project_information"] = getProjectFromName(project)
    return render(request, 'project_page.html', request.session['metadata'])

def pageNotFound(request):
    return render(request, '404.html', request.session['metadata'])

def createProjectSubmit(request):
    data = {
            "description": request.POST.get('description'),
            "sweat": request.POST.get('sweat'),
            "timeframe": request.POST.get('timeframe'),
            "grade": request.POST.get('grade'),
            "tags": {},
            "name": request.POST.get('projectName'),
            "breath": {},
            }

    for i in "BREATH":
        data["breath"][i] = True if request.POST.get(i) == '' else None 

    if request.POST.get('tags'):
        for i in request.POST.get('tags').split(","):
            if not firebase_database.child("listOfTags").child(i).get().val():
                messages.success(request, ('Tag is not in database'))
                return redirect('createproject')
            data["tags"][i] = True

    if data["name"] == '':
        messages.success(request, ('Name is required'))
        return redirect('createproject')

    firebase_database.child("projects").child("potential-projects").child(data["name"].lower().replace(" ", "-")).set(data) 
    return redirect('index')

def getProjectFromName(name):
    try:
        result = firebase_database.child("projects").child("approved-projects").child(name).get().val()
    except:
        try:
            result = firebase_database.child("projects").child("potential-projects").child(name).get().val()
        except:
            result = None

    return result

def projectList(request):
    request.session['metadata']["projects"] = firebase_database.child("projects").child("approved-projects").get().val() 
    return render(request, 'projectlist.html', request.session['metadata'])

def recentProjectsSchools(n):
    projects = firebase_database.child('projects').child('approved-projects').get().val()
    results = {'elementary': [], 'middle': [], 'high': []}
    for key, i in projects.items():
        if len(results['elementary']) < n and (i['grade'] == 'k' or i['grade'] <= 5):
            results['elementary'].append(i)
        if len(results['middle']) < n and 6 <= i['grade'] <= 8:
            results['middle'].append(i)
        if len(results['high']) < n and 9 <= i['grade'] <= 12:
            results['high'].append(i)
        if len(results['high']) == len(results['middle']) == len(results['elementary']) == n:
            break
    return results
