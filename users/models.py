from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 180 or img.width > 180:
            output_size = (180, 180)
            img.thumbnail(output_size)
            img.save(self.image.path)
     

class Asset(models.Model):
    

    name = models.CharField(max_length=100)
    cash_balance = models.FloatField(default=0.0)
    others = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
