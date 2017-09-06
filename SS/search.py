# Import the api module for the results class
import search_google.api
from random import randint

# Define buildargs for cse api
BUILDARGS = {
    'serviceName': 'customsearch',
    'version': 'v1',
    'developerKey': 'AIzaSyBqJ9JPmKVrnjT-9XdTj9R7oKp6HMGN5Cg'
}


def get_search_result_text(q):
    '''
    返回Google Web搜索的结果和url

    q : 搜索关键词<str>

    '''

    # 网页搜索的参数
    cseargs = {
        'q': q,
        'cx': '012122443042025158512:yxwq6atin3w',
        'num': 1
    }

    # 从结果中随机筛选出一条答案
    #n = randint(0, 2)
    n = 0
    results = search_google.api.results(BUILDARGS, cseargs)

    title = results.get_values('items', 'title')
    links = results.get_values('items', 'link')
    snippet = results.get_values('items', 'snippet')

    return '标题：{}\n描述：{}\nlink：{}'.format(title[n], snippet[n].replace('\n', ''), links[n])


def get_search_result_img(q):
    '''
    返回Google Image 搜索的结果url

    q : 搜索关键词<str>

    '''

    # 图片搜索的参数
    cseargs_img = {
        'q': q,
        'cx': '012122443042025158512:yxwq6atin3w',
        'searchType': 'image',
        'fileType': 'jpg',
        'imgType': 'photo',
        'num': 1
    }

    # 从结果中随机筛选出一条答案
    #n = randint(0, 2)
    n = 0
    results = search_google.api.results(BUILDARGS, cseargs_img)

    links = results.get_values('items', 'link')

    return links[n]

