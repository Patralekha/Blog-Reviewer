from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
# -*- coding: utf-8 -*-
#from __future__ import unicode_literals



# Create your models here.
class User(AbstractBaseUser):
    userid=models.AutoField(primary_key=True)
    username=models.CharField(max_length=64)
    email=models.EmailField(max_length=255,unique=True)
    #password=models.CharField(max_length=64)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "{}-{}-{}".format(self.userid,self.username,self.email)


class Blogs(models.Model):
    blogid=models.AutoField(primary_key=True)
    blogname=models.CharField(max_length=200)
    blogtext=models.CharField(max_length=400,blank=True)
    creatorid=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_blog')
    blogimage = models.ImageField(upload_to='images/',null=True)
    likeno=models.IntegerField(default=0)
    dislikeno=models.IntegerField(default=0)
    postdate=models.DateField()
    commentno=models.IntegerField(default=0)

    def __str__(self):
        return "{}-{}-{}".format(self.blogid,self.blogname,self.creatorid)

class UserComments(models.Model):
    commentid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    blogid=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comments=models.CharField(max_length=400,blank=True)
    postedon=models.DateField()

    def __str__(self):
        return "{}-{}-{}-{}".format(self.commentid,self.userid,self.blogid,self.comments)

class UserLikes(models.Model):
    likeid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    blogid=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    like=models.IntegerField(blank=True,default=0)

    def __str__(self):
        return "{}-{}-{}-{}".format(self.likeid,self.userid,self.blogid,self.like)
