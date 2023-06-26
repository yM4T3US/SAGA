from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import *

class Course(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name


class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=16)
    professor = models.BooleanField(default=False)
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/')


    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.first_name 
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("E-mail necessário")
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self.db)
        return user
    




class Discipline(models.Model):
    name = models.CharField(max_length=50)
    access_key = models.CharField(max_length=10)
    semester = models.IntegerField()
    courses = models.ManyToManyField(Course, blank=False, related_name='disciplines')
    #professor = models.ForeignKey(User, blank=False, null=True, related_name='disciplines', on_delete=models.SET_NULL)
    professor = models.ManyToManyField(User, blank=True, null=True, related_name='disciplines')

    def __str__(self) -> str:
        return self.name 
    

class Availability(models.Model):
    initial_datetime = models.DateTimeField(max_length=10, null=True, blank=True)
    final_datetime = models.DateTimeField(max_length=10, null=True, blank=True)
    duration = models.IntegerField( null=True, blank=True)
    professor = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

class Time(models.Model):
    date = models.DateField(max_length=10, null=True, blank=True)
    initial_time = models.TimeField(max_length=10, null=True, blank=True)
    final_time = models.TimeField(max_length=10, null=True, blank=True)
    status = models.BooleanField(max_length=10, null=True, blank=True)
    subject = models.TextField(max_length=250)
    professor = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, related_name="times")
    student = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, )
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)





    

