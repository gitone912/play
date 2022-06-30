
from embed_video.fields import EmbedVideoField
from django.db import models
from django.contrib.auth.models import User
# from fluent_contents.models import PlaceholderField
# from fluent_contents.models import ContentItem
# Create your models here.


class topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class rom(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    participants=models.ManyToManyField(User,related_name='participants')
    updates = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updates','-created']

    def __str__(self):
        return self.name


class message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(rom, on_delete=models.CASCADE)
    body = models.TextField()
    updates = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    
class coursename(models.Model):
    course_name=models.CharField( max_length=50)
    def __str__(self):
        return self.course_name
    

class coursedetails(models.Model):
    cname=models.CharField( max_length=50)
    duration=models.CharField( max_length=50)
    level=models.CharField( max_length=50)
    title = models.CharField(max_length=50,null=True,blank=True)
    link=EmbedVideoField(blank=True,null=True)
    courses=models.ForeignKey(coursename, on_delete=models.CASCADE,related_name='display')

# class Article(models.Model):
#     title=models.CharField( max_length=50)
#     slug=models.SlugField('Slug',unique=True)
#     content=PlaceholderField('article_content')
#     class Meta:
#         verbose_name="Article"
#         verbose_name_plural="Articles"
#     def __unicode__(self):
#         return self.title
    
# class vvp(ContentItem):
#     title=models.CharField( max_length=50)
#     link=models.URLField("URL",max_length=200)
#     class Meta:
#         verbose_name="Article"
#         verbose_name_plural="Articles"
#     def __unicode__(self):
#         return self.title
