from django.conf.urls import url
from . import views


app_name = 'SS'
urlpatterns = [
    url(r'^$', views.wechat, name='wechat'),
]