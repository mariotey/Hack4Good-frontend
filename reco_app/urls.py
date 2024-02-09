from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path('login', views.login_view, name='login'),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 

    path("create_event", views.create_event, name="create_event"),

    path("event/<str:event_title>", views.event, name="event"),
    path("eventreg/<int:event_id>", views.event_reg, name="event_reg"),

    path("user/<str:user_email>", views.get_user, name="user"),
    path("user_edit/<str:user_email>", views.user_edit, name="user_edit"),
    path("user_delete/<str:user_email>", views.user_delete, name="user_delete"),
]