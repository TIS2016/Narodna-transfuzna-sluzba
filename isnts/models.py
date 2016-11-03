from django.db import models
from enum import Enum, unique
from django import forms
from django.contrib.auth.models import User
# Create your models here.

class Blood_type(models.Model):

    @unique
    class Type(Enum):
        a=0
        b=1
        ab=2
        o=3

    TYPE_CHOICES = {
        (Type.a.value,"A"),
        (Type.b.value,"B"),
        (Type.ab.value,"AB"),
        (Type.o.value,"0")
    }

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)


    @unique
    class RH_factor(Enum):
        plus = True
        minus = False

    RH_CHOICES = {
        (RH_factor.plus.value,"+"),
        (RH_factor.minus.value,"-")
    }
    RH = models.BooleanField(choices=RH_CHOICES)

class Address(models.Model):
    ...

class Employee(models.Model):
    ...

class Donor_card(models.Model):
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    id_blood_type = models.ForeignKey(Blood_type,on_delete=models.SET_NULL,null=True)
    phone_num = models.CharField(max_length=20)
    id_address_perm = models.ForeignKey(Address,on_delete=models.PROTECT,null=True,related_name="perm")
    id_address_temp = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,related_name="temp")
    card_created_date = models.DateTimeField(auto_now_add=True)
    card_created_by = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True)
    info = models.CharField(max_length=255)


class Donor(models.Model):
    id_card = models.ForeignKey(Donor_card,on_delete=models.CASCADE)
    active_acount = models.SmallIntegerField(default=0)
    id_user = models.OneToOneField(User)
