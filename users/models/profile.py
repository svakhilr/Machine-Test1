from django.db import models
from .users import CustomUser

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    profile_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.profile_name