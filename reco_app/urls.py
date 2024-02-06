from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"), # Include Full Name

    path("event/<int:event_id>", views.event, name="event"),
    path("eventreg/<int:event_id>", views.event_reg, name="event_reg"),
]