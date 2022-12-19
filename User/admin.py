from django.contrib import admin
from User.models import UserModel
# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display=['id','email','wallet_balance']
admin.site.register(UserModel,UserModelAdmin)