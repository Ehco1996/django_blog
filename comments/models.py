from django.db import models

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # 与post数据库相连接，这里是多对一的关系 用ForeignKey连接到Post类 、
    # 即一个comment只能在一篇post里有，但是一个post里可以有很多comment
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]




