from django.urls import path
from recharge.views import add_recharge_pack

urlpatterns = [
    # path("available", available_packs, name="Available_Packs"),
    path("add", add_recharge_pack, name="Add_Recharge_Pack")

]
