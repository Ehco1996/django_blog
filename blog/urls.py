from django.conf.urls import url

from . import views

#说明该模块是属于blog应用的
app_name = 'blog'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
]