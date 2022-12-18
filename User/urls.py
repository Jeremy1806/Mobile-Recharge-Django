from django.urls import path
from User.views import login, signup

urlpatterns = [
    path("signup", signup, name="Signup"),
    path("login", login, name="Login")
]
