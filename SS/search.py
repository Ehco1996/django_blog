'''
Google Image Spider

'''


# 映入django orm
import sys
import os
import django
sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_blog.settings'
django.setup()

from SS.models import ImageUrl

import requests
from bs4 import BeautifulSoup


SEARCHRUL = 'https://www.google.com/search?&safe=off&q={}&tbm=isch&tbs=itp:photo,isz:l'


def get_html_text(url):
    '''获取网页的原始text'''
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    try:
        r = requests.get(url, timeout=9, headers=headers)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def parse_img_url(q):
    '''
    解析返回搜索图片的原始链接
    q ： 搜索关键词
    nums： 返回的结果数量 最大值20
    '''
    links = []
    url = SEARCHRUL.format(q)
    html = get_html_text(url)
    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find_all('div', class_='rg_meta')
        for link in content:
            rec = eval(link.text)
            links.append(rec['ou'])
        return links
    else:
        return 'error'


from random import sample


def save_img_result(q):
    '''保存数据'''
    links = parse_img_url(q)
    images = ImageUrl.objects.create(name=q, links=links)
    images.save()


def get_image_url(q):
    '''
    检测数据里是否有该关键词的图片
    如果没有，则抓取新的
    '''
    images = ImageUrl.objects.filter(name=q)
    if len(images) != 1:
        res = save_img_result(q)
        return '正在飞速抓取中，请一分钟之后重新输入关键词，获取图片链接'
    else:
        l = sample(eval(images[0].links), 3)
        return '\n\n'.join(x for x in l)
