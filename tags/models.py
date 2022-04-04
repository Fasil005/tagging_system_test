from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # followed_tags = models.ManyToManyField('Tags', related_name='followed_tag', through='ThroughModel')
    # unfollowed_tags = models.ManyToManyField('Tags', related_name='unfollowed_tag', through='ThroughModel')

    class Meta:
        db_table = 'user'


class Tags(models.Model):
    title = models.CharField(max_length=250, unique=True)


class Posts(models.Model):
    title = models.CharField(max_length=100)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    liked_user = models.ManyToManyField(User, related_name='liked_user')
    disliked_user = models.ManyToManyField(User, related_name='disliked_user')
    tagged = models.ManyToManyField(Tags, related_name='tagged')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class FollowedTags(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    is_followed = models.BooleanField(default=True)


class Images(models.Model):
    file = models.ImageField(upload_to='files/')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
