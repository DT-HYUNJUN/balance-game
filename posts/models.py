from django.db import models
from django.conf import settings
import os
from django.conf import settings

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
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

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)