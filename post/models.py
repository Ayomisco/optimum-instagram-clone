from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# 
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse

# for the id
import uuid

# Create your models here.

# Creating file/images path or direcotries
def user_directory_path(instance, filename):
    # This file will be uploaded to MEDIA_ROOT /user(id)/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=80, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('tags', args={self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    likes = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('postdetail', args=[str(self.id)])

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.posted}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.following}"

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = "Follows"

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.date}"

    class Meta:
        verbose_name = 'Stream'
        verbose_name_plural = "Streams"


    # This I'm doing so that anytime a post is made, people following me can as well receive a notification or receive the post
    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        # Filtering all users following me
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()




# Likes Model
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')


post_save.connect(Stream.add_post, sender=Post)
