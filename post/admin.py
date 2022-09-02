from django.contrib import admin
from post.models import *

# Register your models here.
admin.site.register([Tag, Follow, Post, Stream])
# admin.site.register(Tag)
