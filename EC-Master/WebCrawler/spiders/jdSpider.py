# coding:utf-8
from __future__ import unicode_literals
from __future__ import division

__python__ = 3.6

import json
import re
import os
import time
import settings
from WebCrawler.spiderHeart import SpiderHeart
from WebCrawler.webdriver import render_js
from WebCrawler.webdriver import read_page
from DataParser import dataItem


heart = SpiderHeart
goods_list = []

def get_items_id_list(html):
    pattern = re.compile('<a target="_blank" href="//item.jd.com/(.*?).html" onclick=.*?"',re.S)
    obj_list = re.findall(pattern, html)
    return obj_list


def get_comment_json(item_list, key_word, fail_page_que):
    global goods_list
    global heart
    for gid in item_list:
        heart.current_goods_title = goods_list[heart.g_index][0]
        heart.g_index += 1
        comment_url = "http://club.jd.com/comment/productPageComments.action?&productId=%s&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0"%gid
        review_content = read_page(comment_url, detail="jd_%s_%s_1"%(key_word, gid)).decode("gbk").encode("utf-8")
        if not review_content.strip():
            fail_page_que.put((comment_url, key_word, gid, "1"))
            break
        # 遍历单个商品所有能显示的评论
        review_json = json.loads(review_content, strict=False)
        heart.cmt_pages = review_json["maxPage"]
        page_number = review_json["maxPage"]
        print(page_number)
        heart.cmt_index = 1
        if settings.DEBUG:
            print("page:" + str(page_number))
        save_to = os.path.join(settings.json_dir_path, "%s_%s_1.json"%(key_word, gid))
        with open(save_to, "wb") as f:
            f.write(review_content)
        for page in range(2,page_number+1):
            heart.cmt_index = page
            comment_url = "http://club.jd.com/comment/skuProductPageComments.action?"\
                                "&productId={item_id}&score=0&sortType=5&page={page_number}&pageSize=10&isShadowSku=0".format(item_id=gid, page_number=page)
            # Todo: 此处可以添加多线程用于访问评论信息
            review_content = read_page(comment_url, detail="%s_%s_%d"%(key_word, gid, page))  # .decode("gbk").encode("utf-8")
            # 访问失败页面处理
            if not review_content.strip():
                fail_page_que.put((comment_url, key_word, gid, page))
                break
            if settings.DEBUG:
                print(comment_url)
            save_to = os.path.join(settings.json_dir_path, "%s_%s_%d.json"%(key_word, gid,page))
            with open(save_to, "wb") as f:
                f.write(review_content)
            time.sleep(1)
            if settings.DEBUG:
                print("currentPage:",page)


def extract_goods_from_jd_page(HTML):
    """ return: (商品名称，价格，商品id-店铺id元组)"""
    from lxml import etree
    HTML = HTML.decode("utf-8","ignore")
    tree = etree.HTML(HTML)
    goods_warp = tree.xpath('//div[@class="gl-i-wrap j-sku-item"]')
    goods_list = []
    for g in goods_warp:
        goods_name = g.xpath('./div[@class="p-name"]/a[1]/em/text()')
        price = g.xpath('.//*[@class="J_price"]/i/text()')
        url = g.xpath('./div[@class="p-name"]/a[1]/@href')
        if goods_name:
            goods_list.append((goods_name[0].strip(), url[0], price[0]))
    return goods_list


def do_job(url, key_word, fail_page_que, spider_heart):
    """ 解析商品列表页面，提取出必要的商品信息 """
    print(">>>JD spider start working at: {time}".format(time=time.strftime("%Y-%m-%d %H:%M:%S")))
    HTML = render_js(url)
    global goods_list
    goods_list = extract_goods_from_jd_page(HTML)
    if not goods_list:
        return
    pattern = re.compile('//item.jd.com/(\d*?).html',re.S)
    id_list = []
    for item in goods_list:
        goods_id = re.findall(pattern, item[1])
        id_list.append(goods_id[0])
    platform = "TMALL"
    for i in range(len(goods_list)):
        item_id = platform + "_" + key_word + "_" + id_list[i]
        title = goods_list[i][0]
        category = key_word
        price = goods_list[i][2]
        detail = "{update: %s, price: %s}"%(time.strftime("%Y-%m-%d %H:%M:%S"), price) 
        dataItem.Good(
            item_id=item_id, title=title, 
            platform=platform,
            category=category, 
            detail=detail).save_to_db()
    global heart
    heart = spider_heart
    heart.g_num = len(id_list)
    heart.category = key_word
    heart.current_goods_id = id_list[0]
    heart.goods_url = url
    print( "Find %d object in JD: %s"%(len(id_list), url) )
    get_comment_json(id_list, key_word, fail_page_que)
    print("JD spider exits at: {time}>>>".format(time=time.strftime("%Y-%m-%d %H:%M:%S")))
# url = "https://club.jd.com/comment/productPageComments.action?&productId=11519859100&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0"