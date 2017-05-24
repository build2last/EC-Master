# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from ec import JsonAPI

def home(request):
    return HttpResponse("Hello World!")

def aspect_display(request):
    platform = request.GET.get('plat', "")
    return render(request, 'ec/treeMap.html', locals()
    )

def get_aspect_analyse_json(request):
    platform = request.GET.get('plat', "")
    if not platform:
        return HttpResponse("[]", content_type="application/json")
    cmt_num = int(request.GET.get('num', 0))
    by_category = int(request.GET.get('bycate', 0))
    if by_category:
        cate_name = request.GET.get('catename', '')
        json_str = JsonAPI.get_json_by(platform=platform, cmt_num=cmt_num, by_category=True, cate_name=cate_name)
    else:
        json_str = JsonAPI.get_json_by(platform, cmt_num=cmt_num)
    return HttpResponse(json_str, content_type="application/json")

# http://localhost/api/aspect-analyse/query/?plat=jd&num=100&bycate=1&catename=JD~电脑,办公~电脑整机~笔记本