from django.db import models

class RechargePack(models.Model):
    pack_validity : models.IntegerField(verbose_name="Pack Validity", null=False, default=30)
    pack_price : models.IntegerField(verbose_name="Pack Price", null=False)
    pack_operator : models.CharField(verbose_name="Operator" , null=False)
    pack_description : models.CharField(verbose_name="Pack Description", null=False)


 
