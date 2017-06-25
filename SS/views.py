from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
from django.utils.encoding import smart_str
import hashlib
import time

from .handle import main_handle


# Create your views here.

# 公众号自定义的token
TOKEN = 'ehcotest2017'

# csrf_exempt 标记是为了取消django自带的csrf标记


@csrf_exempt
def wechat(request):
    '''
    所有的消息都用进过这个函数进行验证处理
    微信验证的消息是以GET方式获得的
    平时的收发则以POST的方式
    '''

    if request.method == 'GET':
        # 我们来获取微信给我们发送的验证消息
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = TOKEN

        # 按照微信的验证要求将token字段timestamp、nonce字段惊醒字典顺序排序
        # 将三个参数字符串拼接成一个字符串进行sha1加密
        # 获得加密后的字符串可与signature对比，标识该请求来源于微信
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        hashstr = "%s%s%s" % tuple(tmp_list)
        hashstr = hashlib.sha1(hashstr.encode('utf-8')).hexdigest()

        # 如果得出的结果和微信服务器发来的相同，则将echostr返回去
        # 就能成功对接了
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('wx_index')

    if request.method == 'POST':
        # 从微信服务器获得转发来的各种消息

        # 这里将获取到的非uicode字符转换为可以处理的字符编码
        data = smart_str(request.body)
        xml = etree.fromstring(data)

        # 在控制台输出一下挑调试信息
        print('**********收到的XML***********\n')
        print(data)

        response_xml = main_handle(xml)

        return HttpResponse(response_xml)
