import pymysql
import random
import hashlib
import time

HOST = ''
PASSWD = ''
USER=''

def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    '''
    创建指定长度的完全不会重复字符串的
    '''
    random.seed(
        hashlib.sha256(
            ("%s%s%s" % (
                random.getstate(),
                time.time(),
                'SCRWEWYOURBITCHES')).encode('utf-8')
        ).digest())
    return ''.join(random.choice(allowed_chars) for i in range(length))


def gen_money_code(amount):
    con = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWD,
        db='SS',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        code = get_random_string(40)
        with con.cursor() as cursor:
            sql = "INSERT INTO `SS`.`code` (`id`, `code`, `type`, `number`, `isused`, `userid`, `usedatetime`) VALUES (NULL, '{}', '-1', '{}', '0', '0', '1989-06-04 02:30:00');".format(code, amount)
            cursor.execute(sql)
            con.commit()
    finally:
        con.close()
    
    print(code)
    return code

