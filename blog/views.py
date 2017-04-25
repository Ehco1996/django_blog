from django.shortcuts import get_object_or_404, render, HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import markdown

from .forms import AddForm, CommentForm
from .models import Category, Post


# Create your views here.


def index(request):

    # 设置每页显示文章的数量
    limit = 2
    post_list = Post.objects.all()
    # 实例化一个分页对象
    paginator = Paginator(post_list, limit)
    # 获取页码
    page = request.GET.get('page')
    
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:  # 如果页码不是个整数
        contacts = paginator.page(1)
    except EmptyPage:  # 如果页码太大，没有相应的记录
        contacts = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'blog/index.html', context={'contacts':contacts})


def detail(request, pk):
    '''
    这里pk参数和上次编写的一样，都是通过主键id来获取文章
    '''
    post = get_object_or_404(Post, pk=pk)
     
    # 统计阅读数量
    post.count = post.count + 1
    post.save()

   
    
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])

   
    
    # 获取所有文章数量
    post_count = len(Post.objects.all())

    # 获取上下文的
    if post.pk == 1:
        pre_post = {'title': '没有了',
                    'get_absolute_ul': '', }
    else:
        pre_post = get_object_or_404(Post, pk=int(pk) - 1)

    if post.pk == post_count:
        next_post = {'title': '没有了',
                     'get_absolute_ul': '', }
    else:
        next_post = get_object_or_404(Post, pk=int(pk) + 1)

    context = {
        'post': post,
        'pre_post': pre_post,
        'next_post': next_post,
    }

    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
