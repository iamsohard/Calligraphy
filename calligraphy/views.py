from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
import json
import pytz
from datetime import datetime
from .models import History
from django.views import generic
import sys,os
# from .zi2zi import infer_by_text_api

def index(request):
    # print("hello world")
    # 第一个参数是请求对象，第二个参数是模板名，第三个可选参数是字典。它返回使用给定上下文呈现的给定模板的HttpResponse对象。
    return render(request, 'calligraphy/index.html')


def history(request):
    historys = History.objects.order_by('-timeStamp')
    print(historys)
    print(len(historys))
    return render(request, 'calligraphy/history.html', {'historys': historys})


def detail(request, history_id):
    print("show detail", history_id)
    history = History.objects.get(history_id=history_id)
    return render(request, 'calligraphy/detail.html', {'history': history})


def test(request):
    return render(request, 'calligraphy/test.html')


def check_txt(request):
    # print("检测文本")
    content = request.POST.get('content')
    print(content)

    # 将路径保存到数据库中。
    tz = pytz.timezone('Asia/Shanghai')
    t = datetime.now(tz)
    timestamp = t.strftime('%Y-%m-%d %H:%M:%S')
    history_id = t.strftime('%Y%m%d%H%M%S')
    history = History(history_id=history_id)
    history.content = content


    rootpath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(rootpath, 'zi2zi')
    sys.path.append(path)
    history.calligraphy = "static/calligraphy/genimgs/" + history_id + ".jpg"
    import infer_by_text_api
    infer_by_text_api.infer_by_text_api(content,9 ,os.path.join(rootpath,history.calligraphy))

    history.timeStamp = timestamp
    history.info = "info"
    history.save()

    result = []
    result.append(history_id)
    print(result)
    return JsonResponse(json.dumps(result), content_type='application/json', safe=False)


def delete_txt(request, history_id):
    '''
    根据video_id删除对应的视频
    :param request:
    :param video_id:
    :return:
    '''
    print(history_id)
    txts = History.objects.get(history_id=history_id)
    txts.delete()
    # 转发

    # reverse返回某app下某请求的地址
    # print(reverse('calligraphy:history'))
    return HttpResponseRedirect(reverse('calligraphy:history'))