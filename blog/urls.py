from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

# 说明该模块是属于blog应用的
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',
        views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^about/$',views.aboutme,name='aboutme'),
    url(r'^search/$',views.SearchListView.as_view(),name='search'),
    url(r'^tags/(?P<pk>[0-9]+)$',views.TagView.as_view(),name='tag'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
