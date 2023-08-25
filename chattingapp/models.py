from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings  # Import settings
from django.utils import timezone  # Import the timezone module


class ModelGroup(models.Model):
    name = models.CharField( max_length=50)
    
    class Meta:
        verbose_name_plural = "Group of chats"
            
    def __str__(self) :
        return self.name
    
    

class ModelChats(models.Model):
    content= models.CharField( max_length=50)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey("ModelGroup", on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey( User , on_delete=models.CASCADE)
    
    # def __str__(self) :
    #     return self.content
    
    class Meta:
        verbose_name_plural = "Chats"