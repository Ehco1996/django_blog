'''
Google Image Spider

'''


# 引入django orm
import sys
import os
import django
sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_blog.settings'
django.setup()

# 导入数据库model
from SS.models import ImageUrl

# 导入异步requests模块
import asyncio
import aiohttp
import selectors
# 导入解析模块
from bs4 import BeautifulSoup
from random import sample


SEARCHRUL = 'https://www.google.com/search?&safe=off&q={}&tbm=isch&tbs=itp:photo,isz:l'


async def get_html_text_async(url):
    headers = {}
    headers['UseAgent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers=headers) as r:
            return await r.text()


async def parse_img_url(q):
    '''
    解析返回搜索图片的原始链接
    q ： 搜索关键词
    '''

    links = []
    url = SEARCHRUL.format(q)
    #html = get_html_text(url)
    html = await get_html_text_async(url)

    if html != 'error':
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find_all('div', class_='rg_meta')
        for link in content:
            rec = eval(link.text)
            links.append(rec['ou'])
        return links
    else:
        return 'error'


async def save_img_result(q):
    import time
    '''保存数据'''

    links = await parse_img_url(q)
    images = ImageUrl.objects.create(name=q, links=links)
    images.save()


async def get_image_url(q):
    '''
    检测数据里是否有该关键词的图片
    如果没有，则抓取新的
    '''
    images = ImageUrl.objects.filter(name=q)
    if len(images) != 1:
        await save_img_result(q)
        return '正在飞速抓取中，请10s后重新输入关键词，即可获取图片链接'
    else:
        l = sample(eval(images[0].links), 3)
        return '\n\n'.join(x for x in l)


def mainloop(q):
    '''异步执行图片抓取'''

    # 获取异步task，并执行
    selector = selectors.DefaultSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(get_image_url(q))
    loop.close()
    return res
