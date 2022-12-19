from django.urls import path
from User.views import login, signup, recharge_wallet

urlpatterns = [
    path("signup", signup, name="Signup"),
    path("login", login, name="Login"),
    path("wallet",recharge_wallet, name="Wallet Recharge")
]
