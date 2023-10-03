from django.db import models
from datetime import date  # Import the date class

class Registration(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    dob = models.DateField(blank=True, null=True)  
    role = models.CharField(max_length=50)
    jno = models.IntegerField(blank=True, null=True) 
    cdate = models.DateField(blank=True, null=True)
    sal = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=50, unique=True)
    passwd = models.CharField(max_length=50) 
    img = models.ImageField(upload_to="uploads", default="")
    last_login = models.DateTimeField(null=True, blank=True)  # Add last_login field


    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Check if the role is "player" and jno is not provided
        if self.role == "player" and self.jno is None:
            raise ValueError("Jersey number (jno) is required for players.")
        
        super().save(*args, **kwargs)
