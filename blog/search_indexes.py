'''
高亮分词的搜索引擎
配置 django haystack从哪些数据建立索引
以及 索引的存放位置
配置完这个文件之后，我们并不需要去写views和urls，
haystack都帮我们写好了
视图函数会将搜索结果传递给search/search.html
'''

from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex,indexes.Indexable):
    '''
    django haystack规定，要在相对应的app目录下
    创建一个XXIndex类，并继承自（SearchIndex，Indexable）
    '''

    # 每个索引里只要一个字段为document=True，这代表，haystack讲用该字段
    # 来检索文章的内容，而这个字段名一般约定为text
    # use_template 这个属性允许我们使用Django的模板系统传数据回去
    # 模板的路径为：template/search/indexes/blog/post_text.txt

    text = indexes.CharField(document=True , use_template=True)

    def get_model(self):
        return Post
    
    def index_queryset(self,using=None):
        return self.get_model().objects.all()