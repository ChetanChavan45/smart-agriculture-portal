from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('FARMER', 'Farmer'),
        ('EXPERT', 'Agriculture Expert'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='FARMER')
    
    def is_farmer(self):
        return self.role == 'FARMER'
        
    def is_expert(self):
        return self.role == 'EXPERT'
        
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

class Crop(models.Model):
    crop_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    season = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    fertilizer = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    
    def __str__(self):
        return self.crop_name

class FarmerQuery(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    question = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Query by {self.farmer.username}: {self.question[:50]}"

class ExpertResponse(models.Model):
    query = models.OneToOneField(FarmerQuery, on_delete=models.CASCADE, related_name='response')
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response by {self.expert.username} to {self.query.id}"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} {self.action} at {self.timestamp}"
