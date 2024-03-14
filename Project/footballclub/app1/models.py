from datetime import timezone
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
    username = models.CharField(max_length=20, blank=True, null=True, unique=False) 
    role = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Coach(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    cdate = models.DateField(blank=True, null=True)
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to="uploads", default="", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.email

    @property
    def role(self):
        return self.user.role



class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    pos = models.CharField(max_length=50, blank=True, null=True)
    jno = models.IntegerField(blank=True, null=True)
    cdate = models.DateField(blank=True, null=True)
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to="uploads", default="", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.email


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    cdate = models.DateField(blank=True, null=True)
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to="uploads", default="", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return self.user.email
    
class Venue(models.Model):
    venue_id = models.AutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(max_length=254, unique=True)


    def __str__(self):
        return self.name


class Scout(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    cdate = models.DateField(blank=True, null=True)
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to="uploads", default="", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.email


class Opponent(models.Model):
    opponent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE) 
    opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE)
    result = models.CharField(max_length=100, default='upcoming match')


class TrainingSession(models.Model):
    training_id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)  # Link the coach to the session
    venue = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()  
    status = models.CharField(max_length=10, choices=[("unfinished", "Unfinished"), ("finished", "Finished")], default="unfinished")


class PlayerPerformance(models.Model):
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    shoot = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    passing = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    dribble = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    defense = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    physical = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)
    speed = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,blank=True,)

class ScoutedPlayer(models.Model):
    scout = models.ForeignKey(Scout, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    position = models.CharField(max_length=50, choices=[("CF", "Forward"), ("CM", "Midfielder"), ("CD", "Defender"), ("GK", "Goal Keeper")])
    current_status = models.CharField(max_length=10, choices=[("Free", "Free"), ("club", "In a Club")])
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Message(models.Model):
    sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


# models.py
class CoachRequest(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    min_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    max_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)



# models.py
class PlayerDetailsRequest(models.Model):
    coach_request = models.ForeignKey(CoachRequest, on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(ScoutedPlayer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    sal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    position = models.CharField(max_length=50, choices=[("CF", "Forward"), ("CM", "Midfielder"), ("CD", "Defender"), ("GK", "Goal Keeper")])
    current_status = models.CharField(max_length=10, choices=[("Free", "Free"), ("club", "In a Club")])
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    email = models.EmailField()