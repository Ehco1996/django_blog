from django.conf.urls import url
from . import views


app_name = 'SS'
urlpatterns = [
    url(r'^$', views.wechat, name='wechat'),
    url(r'^moneycode/$', views.Money_code_view, name='moneycode'),
    # 支付宝当面付相关:
    url(r'facepay/qrcode/$',views.gen_face_pay_qrcode,name='facepay_qrcode'),

    # 购买处理逻辑
    url(r'facepay/(?P<out_trade_no>[0-9]+)',views.Face_pay_view,name='facepay_view'),

]