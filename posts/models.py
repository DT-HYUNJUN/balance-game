from django.db import models
from django.conf import settings
import os
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    select1_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='select1_posts')
    select1_content = models.CharField(max_length=100)
    select2_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='select2_posts')
    select2_content = models.CharField(max_length=100)

    def post_image_path(instance, filename):
        return f'posts/{instance.pk}/{filename}'
    
    image1 = models.ImageField(blank=True, upload_to=post_image_path)
    image2 = models.ImageField(blank=True, upload_to=post_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    
    def delete(self, *args, **kargs):
        if self.image1:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image1.name))
        if self.image2:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image2.name))
        super(Post, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_review = Post.objects.get(id=self.id)
            if self.image1 != old_review.image1:
                if old_review.image1:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_review.image1.name))
            if self.image2 != old_review.image2:
                if old_review.image2:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_review.image2.name))
        super(Post, self).save(*args, **kwargs)
    
    def select1_count(self):
        try:
            total = (self.select1_users.count() + self.select2_users.count())
            return self.select1_users.count() / total * 100
        except:
            return 0
            
    
    
    def select2_count(self):
        try:
            total = (self.select1_users.count() + self.select2_users.count())
            return self.select2_users.count() / total * 100
        except:
            return 0
        
    
    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')