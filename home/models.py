from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class ExpertiseTags(models.Model):
    expertiseTagName = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.expertiseTagName

    class Meta:
        verbose_name_plural = "Expertise tags"


class Profile(models.Model):
    userId = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    expertiseTags = models.ManyToManyField('ExpertiseTags')

    def __str__(self):
        return f"{self.user}"
    

class SubTags(models.Model):
    subTagName = models.CharField(max_length=50, primary_key=True)
    expertiseTag = models.ManyToManyField('ExpertiseTags')

    def __str__(self):
        return self.subTagName
    
    class Meta:
        verbose_name_plural = "Sub tags"


class Post(models.Model):
    postId = models.AutoField(primary_key=True)
    userId = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="post_user")
    title = models.CharField(max_length=60)
    tags = models.ManyToManyField('SubTags')
    image = models.ImageField(upload_to='media/')
    imageText = models.CharField(max_length=1000)
    assignedUserIds = models.ManyToManyField('Profile', related_name="assigned")

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        img.save(self.image.path)
    

class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    postId = models.ForeignKey('Post', on_delete=models.CASCADE)
    userId = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=1000, null=False)


class Votes(models.Model):
    voteId = models.AutoField(primary_key=True)
    postId = models.ForeignKey('Post', on_delete=models.CASCADE)
    userId = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    positive = models.BooleanField(null=False)

    class Meta:
        verbose_name_plural = "Votes"