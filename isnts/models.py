from django.db import models
from enum import Enum, unique
from django import forms
from django.contrib.auth.models import User
# Create your models here.


class Blood_type(models.Model):

    @unique
    class Type(Enum):
        a = 0
        b = 1
        ab = 2
        o = 3

    TYPE_CHOICES = {
        (Type.a.value, "A"),
        (Type.b.value, "B"),
        (Type.ab.value, "AB"),
        (Type.o.value, "0")
    }

    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    @unique
    class RH_factor(Enum):
        plus = True
        minus = False

    RH_CHOICES = {
        (RH_factor.plus.value, "+"),
        (RH_factor.minus.value, "-")
    }
    RH = models.BooleanField(choices=RH_CHOICES)


class Region(models.Model):

    @unique
    class Regions(Enum):
        Bratislavsky = 0
        Nitriansky = 1
        Trnavsky = 2
        BanskoBystricky = 3
        Zilinsky = 4
        Kosicky = 5
        Presovsky = 6

    REGION_CHOICES = {
        (Regions.Bratislavsky.value,"Bratislavsky"),
        (Regions.Nitriansky.value,"Nitriansky"),
        (Regions.Trnavsky.value,"Trnavsky"),
        (Regions.BanskoBystricky.value,"BanskoBystricky"),
        (Regions.Zilinsky.value,"Zilinsky"),
        (Regions.Kosicky.value,"Kosicky"),
        (Regions.Presovsky.value,"Presovsky")
    }

    name = models.PositiveSmallIntegerField(choices=REGION_CHOICES)

class Address(models.Model):
    city = models.CharField(max_length=50,null=True)
    zip_code = models.CharField(max_length=10,null=True)
    street = models.CharField(max_length=30,null=True)
    number = models.CharField(max_length=10,null=True)
    id_region = models.ForeignKey(Region,on_delete=models.SET_NULL,null=True)

class Office_hours(models.Model):
    ...

class NTS(models.Model):
    name = models.CharField(max_length=30)
    id_address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    location_info = models.CharField(max_length=50,null=True)
    gps_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    gps_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    id_office_hours = models.ForeignKey(Office_hours,on_delete=models.SET_NULL,null=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    other_contact = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    id_boss = models.IntegerField()

class Announcement(models.Model):
    id_nts = models.ForeignKey(NTS,on_delete=models.CASCADE)
    header = models.CharField(max_length=50)
    subheader = models.CharField(max_length=50,null=True)
    text = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

class Employee(models.Model):
    id_nts = models.ForeignKey(NTS,on_delete=models.CASCADE,null=True)
    id_user = models.OneToOneField(User,null=True)
    username = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=30,null=True)

class Donor_card(models.Model):
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    id_blood_type = models.ForeignKey(Blood_type, on_delete=models.SET_NULL, null=True)
    phone_num = models.CharField(max_length=20)
    id_address_perm = models.ForeignKey(
        Address, on_delete=models.PROTECT, null=True, related_name="perm")
    id_address_temp = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="temp")
    card_created_date = models.DateTimeField(auto_now_add=True)
    card_created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    info = models.CharField(max_length=255,null=True)


class Donor(models.Model):
    id_card = models.ForeignKey(Donor_card, on_delete=models.CASCADE)
    active_acount = models.SmallIntegerField(default=0)
    id_user = models.OneToOneField(User)
    username = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)

class Questions(models.Model):
    question_text = models.CharField(max_length=255)

class Questionnaire(models.Model):
    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    height = models.DecimalField(max_digits=6, decimal_places=6)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)

    @unique
    class Gender(Enum):
        male = 0
        female = 1

    GENDER_CHOICES = {
        (Gender.female.value,'female'),
        (Gender.male.value,'male')
    }

    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)

    @unique
    class Answer(Enum):
        yes = 1
        no = 0
        not_sure = 2

    ANSWER_CHOICES = {
        (Answer.no.value,'no'),
        (Answer.yes.value,'yes'),
        (Answer.not_sure.value,'not sure')
    }


class Booking(models.Model):
    id_nts = models.ForeignKey(NTS,on_delete=models.CASCADE)
    id_employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True)
    id_donor = models.ForeignKey(Donor,on_delete=models.CASCADE)
    booking_time = models.DateTimeField()
    id_answer_sheet = models.ForeignKey(Questionnaire,on_delete=models.SET_NULL,null=True)
