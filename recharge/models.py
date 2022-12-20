from django.db import models
from User.models import UserModel
from datetime import date

STATUS_CHOICES = [
    ('Pending','Pending'),
    ('Completed','Completed')
]

class RechargePack(models.Model):
    pack_operator = models.CharField(verbose_name="Operator" ,max_length=150, blank=False)
    pack_price = models.IntegerField(verbose_name="Pack Price", null=False,blank=False,unique=True)
    pack_validity = models.IntegerField(verbose_name="Pack Validity", blank=False)
    pack_description = models.CharField(verbose_name="Pack Description",max_length=150, blank=False)


class MakeRecharge(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="User Object",on_delete= models.CASCADE)
    recharge_pack = models.ForeignKey(RechargePack,verbose_name="Recharge Object" ,on_delete= models.CASCADE)
    phone_number = models.CharField(verbose_name="Mobile Number", blank=False,null=False, max_length=150)
    operator = models.CharField(verbose_name="Mobile Operator", blank=False,null=False, max_length=150)
    price = models.IntegerField(verbose_name="Pack Cost", blank=False,null=False)
    transaction_date = models.DateField(verbose_name="Transaction Date", default=date.today)
    status = models.CharField(verbose_name="Recharge Status", max_length=50, default="Pending" , blank=False, choices=STATUS_CHOICES)

