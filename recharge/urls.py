from django.urls import path
from recharge.views import add_recharge_pack, get_all_packs

urlpatterns = [
    path("packs", get_all_packs, name="Available_Packs"),
    path("add", add_recharge_pack, name="Add_Recharge_Pack")

]
