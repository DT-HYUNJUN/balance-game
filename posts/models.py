from django.db import models
from django.conf import settings

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    select1_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='select1_posts')
    select1_content = models.CharField(max_length=100)
    select2_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='select2_posts')
    select2_content = models.CharField(max_length=100)
    image1 = models.ImageField(blank=True, upload_to=title)
    image2 = models.ImageField(blank=True, upload_to=title)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)