from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, blank=True , null=True, unique=False) 
    age = models.IntegerField(blank=True, null=True)
    role = models.CharField(max_length=50)
    pos = models.CharField(max_length=50, blank=True, null=True)
    jno = models.IntegerField(blank=True, null=True)
    cdate = models.DateField(blank=True, null=True)
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to="uploads", default="", null=True, blank=True)
    email = models.EmailField(primary_key=True,unique=True)
    
   
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    
    def __str__(self):
        return self.email


class Opponent(models.Model):
    opponent_id = models.AutoField(primary_key=True)  # Change to AutoField
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name



class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    venue = models.CharField(max_length=100)
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE)
    result = models.CharField(max_length=100, default='upcoming match')


class TrainingSession(models.Model):
    training_id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the coach to the session
    venue = models.CharField(max_length=100)  
    status = models.CharField(max_length=10, choices=[("unfinished", "Unfinished"), ("finished", "Finished")], default="unfinished")




class PlayerPerformance(models.Model):
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shoot = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    passing = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    dribble = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    defense = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    physical = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    speed = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)