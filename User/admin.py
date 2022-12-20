from django.contrib import admin
from User.models import UserModel
# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display=['id','username','wallet_balance','is_staff']
admin.site.register(UserModel,UserModelAdmin)