from django.shortcuts import get_object_or_404, render,HttpResponse

import markdown

from .forms import AddForm, CommentForm
from .models import Category, Post


# Create your views here.


def index(request):
    post_list = Post.objects.all()
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
    # 生成 评论表单的实例
    form = CommentForm
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list,
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


def test(request):
    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(int(a)+int(b))
    else:
        form = AddForm()
    return render(request, 'blog/test.html', {'form': form})
