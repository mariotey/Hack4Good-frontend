from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from datetime import datetime

# Create your views here.
def index(request):
    cookie_user = request.COOKIES.get("user", "None")

    events = [
        {
            "name": "Disneyland Hongkong",
            "id": 1,
            "description": "fhjgfdsjgfdg;olfdgkzngbjkrgluirzdgiuhzfgnodfzg;ldfzgo;",
            "location": "HarbourFront MRT",
            "start_datetime": datetime(2022, 1, 1, 12, 30, 0),
            "end_datetime": datetime(2022, 1, 2, 12, 30, 0),
            "link": "https://www.hongkongdisneyland.com/?located=true"
        },
        {
            "name": "Disneyland Hongkong",
            "id": 1,
            "description": "fhjgfdsjgfdg;olfdgkzngbjkrgluirzdgiuhzfgnodfzg;ldfzgo;",
            "location": "HarbourFront MRT",
            "start_datetime": datetime(2022, 1, 1, 12, 30, 0),
            "end_datetime": datetime(2022, 1, 2, 12, 30, 0),
            "link": "https://www.hongkongdisneyland.com/?located=true"
        },
        {
            "name": "Disneyland Hongkong",
            "id": 1,
            "description": "fhjgfdsjgfdg;olfdgkzngbjkrgluirzdgiuhzfgnodfzg;ldfzgo;",
            "location": "HarbourFront MRT",
            "start_datetime": datetime(2022, 1, 1, 12, 30, 0),
            "end_datetime": datetime(2022, 1, 2, 12, 30, 0),
            "link": "https://www.hongkongdisneyland.com/?located=true"
        }
    ]

    recomms = [
        {
           "name": "Disneyland Hongkong",
            "id": 1,
            "description": "fhjgfdsjgfdg;olfdgkzngbjkrgluirzdgiuhzfgnodfzg;ldfzgo;",
            "location": "HarbourFront MRT",
            "start_datetime": datetime(2022, 1, 1, 12, 30, 0),
            "end_datetime": datetime(2022, 1, 2, 12, 30, 0),
            "link": "https://www.hongkongdisneyland.com/?located=true"
        }
    ]

    return render(request, 'index.html', {
        "user": cookie_user,
        "events": events,
        "recomms": recomms,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            print("Login successful")

            response = HttpResponseRedirect(reverse("index"))
            response.set_cookie("user", user, max_age=3600)
            return response
        else:
            print("Login unsuccessful")
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    response = HttpResponseRedirect(reverse("index"))
    response.delete_cookie("user")
    return response

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)

            login(request, user)

            return HttpResponseRedirect(reverse("index"))

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username or email already taken."
            })

        except Exception as error:
            print(error)

    else:
        return render(request, "register.html")
    
def event(request, event_id):
    cookie_user = request.COOKIES.get("user", "None")

    event = {
        "name": "Disneyland Hongkong",
        "id": 1,
        "description": "fhjgfdsjgfdg;olfdgkzngbjkrgluirzdgiuhzfgnodfzg;ldfzgo;",
        "location": "HarbourFront MRT",
        "start_datetime": datetime(2022, 1, 1, 12, 30, 0),
        "end_datetime": datetime(2022, 1, 2, 12, 30, 0),
        "link": "https://www.hongkongdisneyland.com/?located=true"
    }

    return render(request, 'event.html', {
        "user": cookie_user,
        "event": event,
        "registered_status": False
    })

def event_reg(request, event_id):
    cookie_user = request.COOKIES.get("user", "None")

    event = {
       "name": "Disneyland Hongkong",
        "id": 1,
        "description": "fhjgfdsjgfdg;olfdgkzngbjkrgluirzdgiuhzfgnodfzg;ldfzgo;",
        "location": "HarbourFront MRT",
        "start_datetime": datetime(2022, 1, 1, 12, 30, 0),
        "end_datetime": datetime(2022, 1, 2, 12, 30, 0),
        "link": "https://www.hongkongdisneyland.com/?located=true"
    }

    return render(request, 'event.html', {
        "user": cookie_user,
        "event": event,
        "registered_status": True
    })