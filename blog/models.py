from django.db import models
#引入django内置的表 User
from django.contrib.auth.models import User
# 导入reverse 函数
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    '''
    规则是一个 Python 类对应一个数据库表格，类名即表名，类的属性对应着表格的列，属性名即列名。

    django 要求我们必须继承 models.Model 类
    Category 目前只需要一个简单的分类名。name就可以了

    CharField 指定了name的数据类型
    即是数据库累心中的字符型
    max_length 制定了该字符的最大长度
    如果超过这个长度，则不能被存入数据库

    django为我们提供了各种数据库需要的类型
    列如下面将要用到的 时间类型 DateTimeField
    其全部的数据类型可以查看起官方文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    '''
    
    name = models.CharField(max_length=100)

    def __str__(self):
        #返回了该表中列的名称
        return self.name

class Tag(models.Model):
    '''
    这个类为标签的数据库表，
    目前也比较简单，只有一列用来存储对应文章id的标签
    '''
    name = models.CharField(max_length=100)
    
    def __str__(self):
        #返回了该表中列的名称
        return self.name

class Post(models.Model):
    '''
    该类为文章类，
    是一个较为复杂的表
    需要记录文章的标题 title 
    正文 body
    发布时间 created_time
    修改时尚 modified_time
    文章摘要 excerpt
    分类 categroy
    标签 tag
    作者 author
    阅读量 count
    '''
    title = models.CharField(max_length=70)
    
    #count 是一个正整数类型，用于记录文章的阅读量。这里使得他自动创建
    count = models.PositiveIntegerField(auto_created=True,default=0)
    
    #图片类型，用来存放上传图片的文件地址
    headimage = models.ImageField(upload_to='head_pic/',default='no-img')
    
    #存储文章正文，用TextField类型来存储长文本
    body = models.TextField()

    #存储文章首页图
    headimage = models.ImageField(
        upload_to='headimg/',
        default='headimg/no-img.jpg',
    )
    
    #这两个列表用来存储时间类型 所以用DateTimeField
    created_time = models.DateTimeField()
    modified_time = models.DateField()

    #这个列用来存储文章的摘要，charfied字段默认是不允许为空的，设置blank属性之后，允许空标题
    excerpt = models.CharField(max_length=200,default='暂无摘要')

    #这是分类的标签
    #分类的标签已经在上面定义过一个专门存放标签的表了
    #这里需要通过外键的形式与之前的表相连接
    #我们规定一篇文章只能对应一个分类，但是一个分来下能有很多篇文章，这就是多对一的关系（ForeignKey
    #但是对于标签来说，
    #一个标签下可以有多个文章 
    #一个文章也可以有多个标签
    #所以我们用（ManyToMany）多对多的方式来连接
    #文档：https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)

    #表示文章作者的列，从django内置表导入
    #django.contrin.auth是django的内置应用
    #专门处理网站用户的注册，登录等流程
    #这里通过ForeignKey将文章和User相连接
    #因为规定一个文章只能有一个作者（author），而一个作者可以有多篇文章
    #所以这里也是一对多的关系
    author =  models.ForeignKey(User)

    def __str__(self):
        #返回了该表中列的名称
        return self.title

    #在url的配置中，设定的name=detatil派上了用场 
    #这个函数的第一个参数（blog：detail）的意思是blog应用下的detail函数，
    #由于我们在上面用app_name=‘bolg’ 告诉了django 这个eurl模块是属于blog的，
    #因此django能找到blog应用下views里的detail函数，从而去试图解析对应的正则 post/(?P<pk>[0-9]+) 
    #这个表达式之后的参数pk 会被后面传入的参数pk替换，如果post的id是255，那么该函数返回post/255/ 从而生成自己的url
    
    
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    
   
            
    
    class Meta:
        ordering = ['-created_time']

