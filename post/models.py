from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    body = models.TextField()

    ## auto time set
    created_time = models.DateTimeField(default = timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    ## latest posts on top
    class Meta:
        ordering = ('-created_time', )

    def __str__(self):
        return self.title
