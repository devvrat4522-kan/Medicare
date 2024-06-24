from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Detail_User_data1(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    adhaar_number = models.CharField(max_length=12, unique=True)
    # password = models.CharField(max_length=255)

    # def __str__(self):
    #     return self.name
    

class Symptom(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField(max_length=255,null=True)
    diet = models.TextField(max_length=255, blank=True, null=True)
    workout = models.TextField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True,null=True)
    precautions = models.TextField(max_length=255, blank=True, null=True)
    disease = models.CharField(max_length=255, blank=True,null=True)
    medication = models.TextField(max_length=255, blank=True, null=True)

    # def __str__(self):
    #     return f"Symptom record for {self.user.name}"

class Contactus(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=255)