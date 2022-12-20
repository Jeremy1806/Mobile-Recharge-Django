from django.db import models

class RechargePack(models.Model):
    pack_operator = models.CharField(verbose_name="Operator" ,max_length=150, blank=False)
    pack_price = models.IntegerField(verbose_name="Pack Price", null=False,blank=False,unique=True)
    pack_validity = models.IntegerField(verbose_name="Pack Validity", blank=False)
    pack_description = models.CharField(verbose_name="Pack Description",max_length=150, blank=False)


 
