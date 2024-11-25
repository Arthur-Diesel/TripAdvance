from django.db import models
from django.contrib.auth.models import User

class TrainedModel(models.Model):
    path = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    mae = models.FloatField(default=0)
    mse = models.FloatField(default=0)
    rmse = models.FloatField(default=0)

    def __str__(self):
        return self.path