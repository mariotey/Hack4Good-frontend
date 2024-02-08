from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path('login', views.login_view, name='login'),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 

    path("create_event", views.create_event, name="create_event"),

    path("event/<int:event_id>", views.event, name="event"),
    path("eventreg/<int:event_id>", views.event_reg, name="event_reg"),
]