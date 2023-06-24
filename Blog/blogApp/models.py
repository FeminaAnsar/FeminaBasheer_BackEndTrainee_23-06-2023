from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

urlpatterns = []



class BlogPost(models.Model):
    title=models.CharField(max_length=255,blank=True)
    description=models.TextField()
    createdDate=models.DateTimeField(default=timezone.now)
    image=models.ImageField(upload_to='uploads/uploads')
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
# Create your models here.
