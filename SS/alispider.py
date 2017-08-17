#!/usr/local/var/pyenv/versions/venv-3.6.1/bin/python
# -*- coding: UTF-8 -*-

# 设置COOK
COOKIES = 'cna=Qy3ZEd8x/kgCAXBXofy0VzLW; NEW_ALIPAY_TIP=1; lzstat_uv=21756086381876643256|2962178; unicard1.vm="K1iSL1vgJ4qYaups+MsoFQ=="; isg=AqWlkIOHEDA2tnRqKOCH-Ij6tGcfSiK5YCuUuaeK8VxWvsYwbzI2RBSePhQz; session.cookieNameId=ALIPAYJSESSIONID; JSESSIONID=B93E2AA3546E0F1CBD2112DA6AD5F7A7; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; ctoken=wMWLGPMsMrA0B_aW; LoginForm=alipay_login_auth; alipay="K1iSL1vgJ4qYaups+MsoFYQBqUJ/vptmLbdK5m3219nhtvsC"; CLUB_ALIPAY_COM=2088202875460101; iw.userid="K1iSL1vgJ4qYaups+MsoFQ=="; ali_apache_tracktmp="uid=2088202875460101"; _hvn_login=1; zone=RZ25B; ALIPAYJSESSIONID=RZ25GRyaX7465vskRzsvQbmMflPrBwauthRZ25GZ00; ALIPAYJSESSIONID.sig=JrSCiyDiZfBaopGFQ6YpM3ES8ImAsAFjklSXHn-6sDE; spanner=4p64KtE6+irsQCZZR3tlRHTy00QmFWvn; rtk=17e4VbrifT4iKVq++7nLEnnj5zuKX+zggscpxDTwaMOSufAklNS'
# 外部文件使用django orm
import sys
import os

import django
sys.path.append('/Users/ehco/Documents/codestuff/learn_django/django_blog')
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_blog.settings'
django.setup()


# 下面就能直接导入models进行操作了
from SS.models import MoneyRecord

import pymysql


def get_money_code(lens):
    '''返回指定数量的10元充值吗'''
    con = pymysql.connect(
        host='*****',
        user='django',
        password='*******',
        db='SS',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with con.cursor() as cursor:
            sql = "select code from code where isused=0 and number=10.00;"
            cursor.execute(sql)
            # 获取一个结果
            result = cursor.fetchall()
    finally:
        con.close()

    # 增加一个简单的判断
    if result:
        money_code = [i['code'] for i in result][:lens]
    else:
        money_code = 'code is out please email me'

    print(money_code)
    return money_code


from aipay_v1 import get_info_code, make_cookies
# 获取账单信息


def add_record():
    '''将支付宝符合信息的数据写入，并生成邀请码'''
    codes = MoneyRecord.objects.all()
    code_list = [i.info_code for i in codes]
    # 获取账单信息

    data = get_info_code(make_cookies(COOKIES))

    # 如果获取到了数据
    if data:
        # 存储符合规则的流水
        clean_data = []
        for i in data:
            amount = i['amount'].replace(' ', '')
            # 符合转入10元的规则
            if i['code'] not in code_list and amount == '+10.00':
                clean_data.append(i)
        # 有符合要求的数据时,从数据库取出对应数量的充值码
        if clean_data:
            money_code = get_money_code(len(clean_data))

            # 保证流水和充值码的数量相等
            if len(money_code) == len(clean_data):
                for i in range(len(money_code)):
                    MoneyRecord.objects.create(
                        info_code=clean_data[i]['code'], amount=clean_data[i]['amount'].replace(' ', ''), money_code=money_code[i])
            else:
                print('code is out please email me')
        else:
            print('no recernt records ')
    else:
        print('cookies dead!')

if __name__ == '__main__':
    add_record()