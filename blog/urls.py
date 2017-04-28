from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

# 说明该模块是属于blog应用的
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',
        views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^about/$',views.aboutme,name='aboutme'),
    url(r'^search/$',views.search,name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
