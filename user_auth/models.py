from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    employee_id = models.TextField(null=True)
    joined_date = models.DateField(null=True)
    date_of_birth = models.DateField(null=True)
    contact_number = models.TextField(null=True)
    address = models.TextField(blank=True, null=True)
    personal_email = models.TextField(blank=True,null=True)
    identity_number = models.TextField(blank=True,null=True)
    passport_number = models.TextField(blank=True,null=True)
    emergency_contact_name = models.TextField(blank=True,null=True)
    emergency_contact_number = models.TextField(blank=True,null=True)
    emergency_contact_relationship = models.TextField(blank=True,null=True)
    leave_annual = models.IntegerField(default=0)
    leave_casual = models.IntegerField(default=0)
    leave_medical = models.IntegerField(default=0)
    leave_other = models.IntegerField(default=0)
    
class ApplyLeave(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.TextField()
    total_days = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    staus = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id