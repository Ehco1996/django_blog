from ..models import Post,Category,Tag
from django import template
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count

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
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)  

@register.simple_tag
def get_recommend_posts(num=3):
    '''
    找到推荐分类的文章的最新三篇
    '''
    return Post.objects.filter(category=1)[:num]
