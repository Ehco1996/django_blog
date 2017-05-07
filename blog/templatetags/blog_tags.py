from ..models import Post,Category
from django import template
from django.shortcuts import get_object_or_404

register = template.Library()


#注册该函数，让我们在模板文件在能使用
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()

@register.simple_tag
def get_recommend_posts(num=3):
    return Post.objects.filter(category=6)[:num]

