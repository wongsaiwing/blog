from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class PostColumn(models.Model):

    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    column = models.ForeignKey(
        PostColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='post'
    )
    tags = TaggableManager(blank=True)
    title = models.CharField(max_length = 50)
    body = models.TextField()

    ## auto time set
    created_time = models.DateTimeField(default = timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    total_views = models.PositiveIntegerField(default=0)


    ## latest posts on top
    class Meta:
        ordering = ('-created_time', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.id])
