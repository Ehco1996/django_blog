from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.six import BytesIO
from PIL import Image

# Create your views here.


def index(request):
    '''
    耳朵转换首页
    '''
    if request.method == 'POST':
        img = request.FILES['imgfile']
        ear_img = get_ear_img(img)
        # 将图片转换为流
        buf = BytesIO()
        ear_img.save(buf, format='PNG')
        image_stream = buf.getvalue()
        # 构造图片reponse
        response = HttpResponse(image_stream, content_type="image/png")
        return response
    else:
        return render(request, 'earimg/index.html', {'filename': '请上传分辨率合适的壁纸图片'})


def get_ear_img(img):
    '''
    将图片加上耳朵
    返会修改过的图片
    '''
    raw_img = Image.open(img)
    raw_img = raw_img.convert('RGBA')
    mask = Image.open(settings.MEDIA_ROOT + '/mask.png')
    mask = mask.convert('RGBA')
    # 获取原图片尺寸
    size = mask.size
    new_img = raw_img.resize(size)
    ear_img = Image.alpha_composite(new_img, mask)
    # 转换后的图片存到本地
    img_path = settings.MEDIA_ROOT + '/earimg/' + \
        img.name.split('.')[0] + '.png'
    ear_img.save(img_path)
    return ear_img
