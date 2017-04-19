from django.contrib import admin
from .models import Post, Category, Tag
from comments.models import Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time',
                    'modified_time', 'category', 'author',]
    search_fields = ['title',]



class PostComment(admin.ModelAdmin):
    list_display=['name','text','url','created_time']


# Register your models here.


admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, PostComment)
