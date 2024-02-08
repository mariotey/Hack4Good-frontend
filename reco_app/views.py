from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import requests

from datetime import datetime

FASTAPI_BASE_URL = "http://localhost:8000"

# Create your views here.
def index(request):
    cookie_user = request.COOKIES.get("user_email", "None")

    if cookie_user == "None":
        admin_status = False
    else:
        admin_status = requests.get(
            f"{FASTAPI_BASE_URL}/user/is_admin", 
            params={"email": cookie_user}
        ).json()["is_admin"]

    events = requests.get(
        f"{FASTAPI_BASE_URL}/event/get_events", 
    ).json()["event_titles"]

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
        "user_email": cookie_user,
        "admin_status": admin_status,
        "events": events,
        "recomms": recomms,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        login_data = {
            "email": request.POST["email"],
            "password": request.POST["password"]
        }
        
        try:
            # Check if authentication successful
            fastapi_response = requests.post(
                f"{FASTAPI_BASE_URL}/login", 
                json=login_data
            ).json()

            print(f"\n{fastapi_response["message"]}\n")

            response = HttpResponseRedirect(reverse("index"))
            response.set_cookie("user_email", request.POST["email"], max_age=3600)
            return response
        except:
            print("Login unsuccessful")
            return render(request, "login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)

    print("Logout successfully")

    response = HttpResponseRedirect(reverse("index"))
    response.delete_cookie("user_email")
    return response

def register(request):
    if request.method == "POST":
        if request.POST["password"] != request.POST["confirmation"]:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        register_data = {
            "email": request.POST["email"],
            "full_name": request.POST["full_name"],
            "password": request.POST["password"],
            "age": int(request.POST["age"]),
            "gender": request.POST["gender"],
            "phone_number": request.POST["phone_number"],
            "work_status": request.POST["work_status"],
            "immigration_status": request.POST["immigration_status"],
            "skills": request.POST["skills"],
            "interests": request.POST["interests"],
            "past_volunteer_experience": request.POST["past_volunteer_experience"],
        }

        # Attempt to create new user
        try:
            fastapi_response = requests.post(
                f"{FASTAPI_BASE_URL}/register", 
                json=register_data
            ).json()

            print(f"\n{fastapi_response["message"]}\n")

            response = HttpResponseRedirect(reverse("index"))
            response.set_cookie("user_email", request.POST["email"], max_age=3600)
            return response

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username or email already taken."
            })

        except Exception as error:
            print(error)
            return render(request, "register.html", {
                "message": "An error occurred."
            })

    else:
        return render(request, "register.html")

def create_event(request):
    """
    Navigates to Event Creation page
    """

    if request.method == "POST":
        new_event_data = {
            "email": request.POST["email"],
            "title": request.POST["title"],
            "date": request.POST["date"],
            "time": request.POST["time"],
            "requirements": request.POST["requirements"],
            "capacity": int(request.POST["capacity"]),
            "deadline": request.POST["deadline"],
            "location": request.POST["location"],
            "description": request.POST["description"],
            "tasks": request.POST["tasks"],
        }

        try:
            fastapi_response = requests.post(
                f"{FASTAPI_BASE_URL}/event/create_event", 
                json=new_event_data
            ).json()
            
            print(f"\n{fastapi_response['message']}\n")

            response = HttpResponseRedirect(reverse("index"))
            response.set_cookie("user_email", request.POST["email"], max_age=3600)
            return response

        except:
            return render(request, "createEvent.html", {
                "message": "Error in creating event"
            })
    else:
        return render(request, 'createEvent.html')
  
def event(request, event_id):
    """
    Navigates to Event Page
    """
    
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
    """
    Registration Mechanism for Event Page, TBC
    """
    
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
