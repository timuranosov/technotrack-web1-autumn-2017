from django.contrib import admin
from .models import Forum, Topic, Post, Category

# Register your models here.

admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Category)