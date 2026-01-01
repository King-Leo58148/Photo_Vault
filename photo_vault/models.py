from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage
class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)


class Album(models.Model):
    album_name=models.CharField(max_length=25,null=True,blank=True)
    
    def __str__(self):
        return self.album_name or "Unnamed Album"

class Photo(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=25)
    description=models.TextField()
    photo=models.ImageField(storage=MediaCloudinaryStorage(),upload_to="photos/")
    private=models.BooleanField(default=True)
    album=models.ForeignKey(Album,on_delete=models.DO_NOTHING,null=True,blank=True)
    def __str__(self):
        return self.title
