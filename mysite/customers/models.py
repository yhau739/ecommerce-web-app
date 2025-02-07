from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Use auto_now_add to set the creation date automatically

    def __str__(self):
        return f"{self.user.username} "
