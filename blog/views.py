from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.views.generic import ListView, DetailView
import markdown


from comments.forms import CommentForm
from .models import Category, Post,Tag


# Create your views here.


class IndexView(ListView):
    '''
    首页的类视图
    继承自Listview
    该类用于表示从数据库获取的模型列表
    '''
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'contacts'
    # 该参数可以激活ListView内置的页面导航模板 这里设置为每页显示10条项目
    paginate_by = 10

    def get_context_data(self, **kwargs):
        '''
        在视图函数中，将模板变量传输给木变是通过render函数的context参数 传输一个字典实现的
        在类视图中，这个方法需要传递给模板变量的字典 是通过 get_context_data 方法获得的，
        在这里我们需要复写该方法，从而能插入一些我们需要的变量进去
        '''

        # 首先获得父类生成的 字典
        context = super().get_context_data(**kwargs)

        # 父类生成的字典已有 pageinator paga_obj is_paginated 这三个模板变量
        # pageinator 是Paginator的一个实例，
        # page_obj 是Page的一个实例
        # is_pageinator 是一个布尔型变量，用于指示是否已经分页
        # 例如如果规定每页需要10个数据，但实际上只有5个数据，那么久不需要分页：
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个对应的键值
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页需要的导航栏数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条模板变量更新到 context中，pagination_data返回的也是一个字典
        context.update(pagination_data)

        # 最后将context返回，让ListView 使用这个字典中的模板变量去渲染模板
        # 注意，此时的 context字典中 已经有了渲染导航小所需要的数据
        return context

    def pagination_data(self, paginator, page, is_paginated):
        '''
        生成页码导航栏所需要的数据
        '''

        if not is_paginated:
            # 如果没有分页，则无需显示导航栏，因此返回一个空的字典
            return {}

        # 当前页的左边连续的 页码号 初始化为{}
        left = []
        # 当前页的右边连续的 页码号 初始化为{}
        right = []

        # 表示第一页后面，是否需要显示 省略号
        left_has_more = False
        # 表示最后一页后面，是否需要显示 省略号
        right_has_more = False

        # 表示是否需要显示第一页的页码号
        # 如果当前页的左边连续页码号中已经含有第 1 页的页码号，此时就无需再显示了
        # 在其他的情况下默认都是要显示第一页的页码
        first = False

        # 表示是否要显示最后一页的页码号
        last = False

        # 获取当前用户请求的页码编号
        page_number = page.number

        # 获取分页的总页数：
        total_pages = paginator.num_pages

        # 获取整个分页的页码列表，比如分了四页 那就是[1,2,3,4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户秦秋的是第一页的数据，那么当前页的左边不需要数据，因此left=[]（默认）
            # 此时只要获取当前页码右边的连续页码号
            # 比如分页列表里是[1,2,3,4] 这里就需要获取 right=[2,3]
            # 注意，这里是获取了当前页码后的连续两个页码
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码比最后一页的页码-1还要小，
            # 说明组右边的页码号和最后一页的页码好之间还有其他页码，此时需要显示省略号
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码好比最后一页的页码小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果当前页是最后一页的数据，那么右边就不需要显示数据 因此right=[] (默认)
            # 此时只需要显示左边的连续页码号
            # 比如分页也码表是[1,2,3,4]那么获取的就是[2,3]

            left = page_range[(page_number - 3)
                              if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果左边的页码号比第 2 页 的页码号大，说明当前连续页码中不包含第一页 所以需要显示左边的省略号和第一页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            # 如果用户请求的不是第一页 也不是最后一页，则需要获取当前页左右两边的页码号
            # 这里默认显示的显示当前页码前后两个页码
            left = page_range[(page_number - 3)
                              if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第1页和第一页后面的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


def index(request):

    # 设置每页显示文章的数量
    limit = 10
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

    return render(request, 'blog/index.html', context={'contacts': contacts})


class PostDetailView(DetailView):
    '''
    详情页面类视图，
    继承自 DetailView
    该类表示冲数据库中获得某一条数据
    '''
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 复写了get 方法的目的是每当文章访问一次，我们即将将文章的阅读量+1
        # get 方法返回一个 HttpREsponse实例
        # 我们需要先调用父类的get方法，这才能有self.objecet的属性。
        # 其值为Post 即我们将要访问的post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将阅读量+1
        # 这里的self.object的值就是被访问的文章 post
        self.object.increase_count()

        # 将Response对象返回
        return response

    def get_object(self, queryset=None):
        # 复写 get_object 方法是为了对post的body进行渲染，
        post = super(PostDetailView, self).get_object(queryset=None)

        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 复写 get_contex_data 是为了除了将post传递给模板外（DetailView已经帮我们完成）
        # 还要讲我们自己写的其他数据传递给模板，如评论表单，上下文等
        context = super(PostDetailView, self).get_context_data(**kwargs)

        
        # 获取上下文的
        # 需要注意上下文可能不存在，需要处理异常
        try:
            pre_post = self.object.get_previous_by_created_time()
        except self.object.DoesNotExist:
            pre_post = None
        
        try:
            next_post = self.object.get_next_by_created_time()
        except self.object.DoesNotExist:
            next_post = None

        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
            'pre_post': pre_post,
            'next_post': next_post,
        })

        return context


def detail(request, pk):
    '''
    这里pk参数和上次编写的一样，都是通过主键id来获取文章
    '''
    post = get_object_or_404(Post, pk=pk)

    # 统计阅读数量 注意 要在渲染markdown之前使用
    post.increase_count()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])

    post.body = md.convert(post.body)

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

     # 实例化评论模型
    form = CommentForm()
    # 获取这篇文章下单所有评论
    comment_list = post.comment_set.all()

    context = {
        'post': post,
        'pre_post': pre_post,
        'next_post': next_post,
        'comment_list': comment_list,
        'form': form,
    }

    return render(request, 'blog/detail.html', context=context)


class ArchivesView(ListView):
    '''
    归档页面的类视图
    '''
    model = Post
    template_name = 'blog/result.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


def archives(request, year, month):
    contacts = Post.objects.filter(
        created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'contacts': contacts})


class CategoryView(ListView):
    '''
    分类页面的类视图
    '''
    model = Post
    template_name = 'blog/result.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        '''
        从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，
        非命名组参数值保存在实例的 args 属性（是一个列表）里。
        所以我们使了 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。
        然后我们调用父类的 get_queryset 方法获得全部文章列表，
        紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。
        '''
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    contacts = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'contacts': contacts})


def aboutme(request):
    return render(request, 'blog/about.html', context=None)


class SearchListView(ListView):
    model = Post
    template_name = 'blog/result.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwrags):
        context = super(SearchListView, self).get_context_data(**kwrags)
        q = self.request.GET.get('q')
        post_list = Post.objects.filter(title__icontains=q.upper())
        context.update({'post_list': post_list})
        return context


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词:"
        return render(request, 'blog/result.html', context={'error_msg': error_msg, })
    else:

        post_list = Post.objects.filter(title__icontains=q.upper())
        return render(request, 'blog/result.html', context={'errot_msg': error_msg,
                                                            'post_list': post_list,
                                                            })

class TagView(ListView):
    '''
    显示某一个标签下的所有文章
    '''
    model = Post
    template_name='blog/result.html'
    context_object_name='post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)