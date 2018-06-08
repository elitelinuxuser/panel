from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import time
from datetime import datetime, timezone
import pytz
from pprint import pprint

config = {
    'apiKey': "AIzaSyBZjYeFAlMZXZpUwkmrfJ3mGKPrrZkT5Ao",
    'authDomain': "cpanel-9b872.firebaseapp.com",
    'databaseURL': "https://cpanel-9b872.firebaseio.com",
    'projectId': "cpanel-9b872",
    'storageBucket': "cpanel-9b872.appspot.com",
    'messagingSenderId': "144185698279"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()

def signIn(request):
    if(authe.current_user):
        email = authe.current_user['email']
        return render(request,'welcome.html', {'email':email})
    return render(request,'signIn.html')

def postsign(request):
    if(authe.current_user):
        email = authe.current_user['email']
        return render(request,'welcome.html', {'email':email})
    email = request.POST.get('email')
    password  = request.POST.get('password')

    try:
        user = authe.sign_in_with_email_and_password(email,password)
    except:
        message = "Invalid credentials!"
        return render(request,'signIn.html',{'message':message})
    pprint(vars(authe.requests))
    session_id = user['idToken']
    request.session['uid']=str(session_id)
    return render(request,'welcome.html',{"email":email})

def logout(request):
    auth.logout(request)
    print(authe.current_user)
    return render(request,'signIn.html')

def signUp(request):
    return render(request,'signup.html')

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password  = request.POST.get('password')

    try:
        usr = authe.create_user_with_email_and_password(email,password)
    except:
        message = 'unable to create account try again'
        return render(request,'signup.html',{'message':message})

    uid = usr['localId']
    data = {'name':name, 'status':'1'}
    database.child('users').child(uid).child('details').set(data)
    message = 'Sign Up Successful!'
    return render(request,'signIn.html', {'message':message})

def create(request):
    return render(request,'create.html')

def postcreate(request):
    p_name = request.POST.get('p_name')
    measure = request.POST.get('measure')
    desc = request.POST.get('desc')
    optradio = request.POST.get('optradio')
    price = request.POST.get('price')

    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print(time_now)

    data = {
        'pname':p_name,
        'measure':measure,
        'desc':desc,
        'optradio':optradio,
        'price':price,
    }

    return render(request,'welcome.html',data)
