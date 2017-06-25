'''
从数据库里查询邀请码
'''
import pymysql.cursors
import time
from django.template.loader import render_to_string


# 和数据库相连接

def get_invite_code():
    con = pymysql.connect(
        host='****',
        user='django',
        password='******',
        db='SS',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with con.cursor() as cursor:
            sql = "select code from ss_invite_code where user_id=484;"
            cursor.execute(sql)
            # 获取一个结果
            result = cursor.fetchone()
    finally:
        con.close()

    # 增加一个简单的判断
    if result:
        invite_code = result['code']
    else:
        invite_code = '当前邀请码已经彻底用完，请在后台联系我'

    print(invite_code)
    return invite_code


def code_back(xml):
    '''
    处理微信发来的数据，
    这里仅仅返回用户发来的消息
    str 是微信服务器post来的xml格式的数据

    返回处理过的xml
    '''

    # 我们翻转发件人和收件人的消息
    fromUser = xml.find('ToUserName').text
    toUser = xml.find('FromUserName').text
    content = get_invite_code()
    message_id = xml.find('MsgId').text

    # 我们来构造需要返回的时间戳
    nowtime = str(int(time.time()))

    context = {
        'FromUserName': fromUser,
        'ToUserName': toUser,
        'Content': content,
        'time': nowtime,
        'id': message_id,
    }
    # 我们来构造需要返回的xml
    respose_xml = render_to_string('SS/wx_text.xml', context=context)

    return respose_xml
