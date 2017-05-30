from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm

from blog.models import Post

from .models import Comment

# Create your views here.


def post_comment(request, post_pk):
    # 这里先过去被评论的文章，因为后面需要把评论和文章关联起来
    # 这里我们使用了django内置的函数get_objects_or_404
    # 从而获取post类 也就是文章详情
    post = get_object_or_404(Post, pk=post_pk)

    # http协议中只有post和get方法，2而表单的数据传输都是用过 post 请求，
    # 所以这里我们选择当 请求 为post是才处理表单数据
    if request.method == 'POST':
        # 用户评论时提交的数据 存在 request.POST
        # 我们利用这个数据结构 CommentForm 的实例，这样生成了field字段的（name email texe url）
        form = CommentForm(request.POST)

        # 通过is_vaild()方法，django 会帮我们检测数据内容是否合法
        if form.is_valid():
            # 当数据合法时候，我们调表单的save方法 将其存入数据库
            # commit = False 的作用是 利用表单数据，成成 Comment 模型的实例
            # 意思是 目前不把form里的内容提交到数据库
            comment = form.save(commit=False)
            # 将评论和文关联起来
            comment.post = post
            # 最后将commen模型的数据保存到数据库
            comment.save()

            # 保存之后 重定向网页 重新渲染
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染本页面，并渲染出表单的错误
            # 因此我们穿了三个变量给 detail 模板，
            # Post （文章） 平路列表 表单Form
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)

    # 不是 psot 请求，说名用户没有提交数据，重定向到文章详情页
    return redirect(post)
