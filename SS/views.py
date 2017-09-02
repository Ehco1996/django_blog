from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.six import BytesIO
from django.contrib import messages
from lxml import etree
from django.utils.encoding import smart_str
import hashlib
import time
import datetime

from .handle import main_handle
from .models import MoneyRecord
import qrcode

from .ss_code import gen_money_code
from .payments import alipay
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

        # 调用我们的handle函数来处理xml
        response_xml = main_handle(xml)

        return HttpResponse(response_xml)


def Money_code_view(request):
    '''返回充值码'''

    context = {}

    if request.method == 'POST':
        number = request.POST.get('q')
        out_trade_no = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y%m%d%H%M%S%s')
        try:
            # 获取金额数量
            amount = int(number)
            # 生成订单
            trade = alipay.api_alipay_trade_precreate(
                subject="Ehco的{}元充值码".format(amount),
                out_trade_no=out_trade_no,
                total_amount=amount,
                timeout_express='60s',)

            # 获取二维码链接
            code_url = trade.get('qr_code', '')
            request.session['code_url'] = code_url
            # 将订单号传入模板
            context['out_trade_no'] = out_trade_no
            context['info'] = '请用支付宝扫描下方二维码付款 付费完成之后请点击确认!'
        except:
            res = alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)

    else:
        context['info'] = '请输入金额后点击提交，生成支付订单二维码,扫描二维码付费后点确认，即可获得等额的充值码'
    return render(request, 'SS/moneycode.html', context=context)


def gen_face_pay_qrcode(request):
    '''生成当面付的二维码'''
    # 从seesion中获取订单的二维码
    url = request.session.get('code_url', '')
    # 删除订单二维码
    del request.session['code_url']
    # 生成ss二维码
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    # 构造图片reponse
    response = HttpResponse(image_stream, content_type="image/png")

    return response


def Face_pay_view(request, out_trade_no):
    '''当面付处理逻辑'''
    context = {}
    paid = False

    for i in range(10):
        time.sleep(3)
        # 每隔三秒检测交易状态
        res = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if res.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            amount = res.get("total_amount", 0)
            # 生成对于数量的充值码
            moneycode = gen_money_code(amount)
            # 后台数据库增加记录
            record = MoneyRecord.objects.create(
                info_code=out_trade_no, amount=amount, money_code=moneycode)
            # 返回充值码到网页
            messages.info(request, '充值码生成成功，请尽快复制充值！')
            messages.success(request, moneycode)
            return HttpResponseRedirect('/wechat/moneycode/')
    # 如果30秒内没有支付，则关闭订单：
    if paid is False:
        alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)
        messages.warning(request, "充值失败了!自动跳转回充值界面")
        return HttpResponseRedirect('/wechat/moneycode/')
