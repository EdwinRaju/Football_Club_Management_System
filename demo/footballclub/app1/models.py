
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, blank=True , null=True, unique=False) 
    dob = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=50)
    jno = models.IntegerField(blank=True, null=True)
    cdate = models.DateField(blank=True, null=True)
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to="uploads", default="")
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email