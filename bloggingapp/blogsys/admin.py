#from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . models import User,Blogs,UserComments,UserLikes

admin.site.register(User)
admin.site.register(Blogs)
admin.site.register(UserComments)
admin.site.register(UserLikes)
