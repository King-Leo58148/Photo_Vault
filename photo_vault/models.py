from django.db import models
from django.contrib.auth.models import User
class Photo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=25)
    description=models.TextField()
    photo=models.ImageField(upload_to="photos/")
    def __str__(self):
        return self.title
