from django.conf.urls import url
from . import views


app_name = 'SS'
urlpatterns = [
    url(r'^$', views.wechat, name='wechat'),
    url(r'^moneycode/$', views.Money_code_view, name='moneycode'),
]