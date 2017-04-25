from django.shortcuts import get_object_or_404, render, HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import markdown

from .forms import AddForm, CommentForm
from .models import Category, Post


# Create your views here.


def index(request):
    '''
    limit = 3  # 每页显示的记录数
    topics = Topic.objects.all()
    paginator = Paginator(topics, limit)  # 实例化一个分页对象

    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render_to_response('index.html', {'topics': topics})
    '''
    limit = 5
    post_list = Post.objects.all()
    pagunator = Paginator(post_list,limit) #实例化一个分页对象

    page = request.GET.get('page') #获取页码

    try:
        post_list = pagunator.page(page)
    except PageNotAnInteger: #如果页码不是个整数
        post_list = pagunator.page(1)
    except EmptyPage:  # 如果页码太大，没有相应的记录
        post_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    '''
    这里pk参数和上次编写的一样，都是通过主键id来获取文章
    '''
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])

    post.count = post.count + 1
    post.save()

    return render(request, 'blog/detail.html', context={'post': post})


def archives(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
