from django.db import models
from user_auth.models import CustomUser
# Create your models here.
class Shift(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.id
    
class Prediction(models.Model):
    id = models.AutoField(primary_key=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    suprise = models.DecimalField(max_digits=5, decimal_places=2)
    sad = models.DecimalField(max_digits=5, decimal_places=2)
    netural = models.DecimalField(max_digits=5, decimal_places=2)
    happy = models.DecimalField(max_digits=5, decimal_places=2)
    fearful = models.DecimalField(max_digits=5, decimal_places=2)
    disgusted = models.DecimalField(max_digits=5, decimal_places=2)
    angry = models.DecimalField(max_digits=5, decimal_places=2)
    stress = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.id