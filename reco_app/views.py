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
    user_email = request.COOKIES.get("user_email", "None")

    if user_email == "None":
        admin_status = False
        recomms = []
        registered = []
        username = "None"
    else:
        admin_status = requests.get(
            f"{FASTAPI_BASE_URL}/user/is_admin", 
            params={"email": user_email}
        ).json()["is_admin"]

        recomms = requests.get(
            f"{FASTAPI_BASE_URL}/user/get_similar_events", 
            params={"email": user_email}
        ).json()["top_5_events"]

        registered = requests.get(
            f"{FASTAPI_BASE_URL}/user/get_user_events", 
            params={"email": user_email}
        ).json()["events_registered"]

        username = requests.get(
            f"{FASTAPI_BASE_URL}/user/get_user", 
            params={"email": user_email}
        ).json()["full_name"]

    response = render(request, "index.html",{
        "username": username,
        "user_email": user_email,
        "admin_status": admin_status,
        "events": requests.get(
                        f"{FASTAPI_BASE_URL}/event/get_events", 
                    ).json()["event_titles"],
        "registered": registered,
        "recomms": recomms,
    })

    response.set_cookie("username", username, max_age=3600)

    return response

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

            print(f"\n{fastapi_response['message']}\n")

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
    response.delete_cookie("username")
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

            print(f"\n{fastapi_response['message']}\n")

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
  
def event(request, event_title):
    """
    Navigates to Event Page
    """
    
    cookie_user = request.COOKIES.get("user_email", "None")
    username = request.COOKIES.get("username", "None")

    event = requests.get(
        f"{FASTAPI_BASE_URL}/event/get_event", 
        params={"title":event_title}
    ).json()

    return render(request, 'event.html', {
        "username": username,
        "user_email": cookie_user,
        "event": event,
        "registered_status": False
    })

def event_reg(request, event_id):
    """
    Registration Mechanism for Event Page, TBC
    """
    
    cookie_user = request.COOKIES.get("user_email", "None")

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
        "user_email": cookie_user,
        "event": event,
        "registered_status": True
    })

def get_user(request, user_email):
    user_email = request.COOKIES.get("user_email", "None")
    username = request.COOKIES.get("username", "None")
    
    user_details = requests.get(
        f"{FASTAPI_BASE_URL}/user/get_user", 
        params={"email": user_email}
    ).json()

    user_admin  = requests.get(
        f"{FASTAPI_BASE_URL}/user/is_admin", 
        params={"email": user_email}
    ).json()["is_admin"]

    print(user_admin)

    return render(request, 'user.html', {
        "username": username,
        "user_email": user_email,
        "user_details": user_details,
        "user_admin": user_admin,
    })


def user_edit(request, user_email):
    user_email = request.COOKIES.get("user_email", "None")
    username = request.COOKIES.get("username", "None")

    if request.method == "POST":
        update_data = {
            "email": request.POST["email"],
            "full_name": request.POST["full_name"],
            # "password": request.POST["password"],
            "age": int(request.POST["age"]),
            "gender": request.POST["gender"],
            "phone_number": request.POST["phone_number"],
            "work_status": request.POST["work_status"],
            "immigration_status": request.POST["immigration_status"],
            "skills": request.POST["skills"],
            "interests": request.POST["interests"],
            "past_volunteer_experience": request.POST["past_volunteer_experience"],
        }
        
        ## Update API request

        response = HttpResponseRedirect(reverse("get_user"))
        response.set_cookie("user_email", request.POST["email"], max_age=3600)
        return response

    else:
        user_details = requests.get(
            f"{FASTAPI_BASE_URL}/user/get_user", 
            params={"email": user_email}
        ).json()

        return render(request, 'user_edit.html', {
            "username": username,
            "user_email": user_email,
            "user_details": user_details,
        })
    
def user_delete(request, user_email):

    fastapi_response = requests.post(
        f"{FASTAPI_BASE_URL}/user/delete_user", 
        json={'email': str(user_email)}
    ).json()
    
    response = HttpResponseRedirect(reverse("index"))
    response.delete_cookie("user_email")
    response.delete_cookie("username")

    print(f"\n{fastapi_response['message']}\n")

    return response
