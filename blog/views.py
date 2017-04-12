from django.shortcuts import render

from .models import Post

from django.shortcuts import render, get_object_or_404
# Create your views here.


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})



def detail(request, pk):
    # pk的意思是主键，即从url获取文章id
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', context={'post': post})


