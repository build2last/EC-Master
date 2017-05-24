# coding:utf-8

""" 天猫商品评论页面数据解析 """

from __future__ import unicode_literals
from __future__ import division

__python_version__ = "3.6"

import re
import time
import json
import settings
from WebCrawler.webdriver import read_page, render_js
import WebCrawler.webdriver as wd
from DataParser import dataItem


def object_get_from_html(html):
    pattern = re.compile('<a href="//detail.*?id=(?P<id>.*?)&.*?user_id=(?P<user_id>.*?)&.*?"',re.S) #r'<a href="//detail.tmall.com/item.htm?id=(?P<id>.*?)&.*?user_id=(?P<user_id>.*?)&
    obj_list = re.findall(pattern,html)
    return obj_list

    
def get_review_from_api(id_tuple_list, key_word, fail_page_que):
    import os
    global heart
    for atuple in id_tuple_list:
        try:
            heart.g_index += 1
            heart.cmt_index = 1
            page = 1
            review_url = "https://rate.tmall.com/list_detail_rate.htm?itemId={goods_id}&sellerId={sellerId}" \
                "&order=3&currentPage={page_number}&append=0&content=1&callback=jsonp734".format(goods_id=atuple[0], sellerId = atuple[1], page_number=1)
            review_content = read_page(review_url, detail="%s_%s_%d"%(key_word, atuple[0], page))
            review_content = review_content.decode("gbk", "ignore").strip()[9:-1]
            if "anti_Spider" in review_content:
                raise Exception("Anti-spider page!")  
            save_to = os.path.join(settings.json_dir_path, "%s_%s_%d.json"%(key_word, atuple[0], page))
            with open(save_to, "w") as f:
                f.write(review_content)
            review_json = json.loads(review_content, strict=False)
            page_number = review_json["rateDetail"]["paginator"]["lastPage"]
            heart.cmt_pages = page_number
            if settings.DEBUG:
                print("page:" + str(page_number))
            for page in range(2,page_number+1):
                heart.cmt_index = page
                try:
                    review_url = "https://rate.tmall.com/list_detail_rate.htm?itemId={goods_id}&sellerId={sellerId}" \
                      "&order=3&currentPage={page_number}&append=0&content=1&callback=jsonp734".format(goods_id=atuple[0], sellerId = atuple[1], page_number=page)    
                    review_content = read_page(review_url, detail="%s_%s_%d"%(key_word, atuple[0], page)).decode("gbk", "ignore").strip()[9:-1]
                    # 反爬虫检测页面探测
                    if "anti_Spider" in review_content:
                        fail_page_que.put((review_url, key_word, atuple[0], page))
                        print("Detect Anti-spider page in Tmall spider!")
                        continue
                    save_to = os.path.join(settings.json_dir_path, "%s_%s_%d.json"%(key_word, atuple[0], page))
                    with open(save_to, "w") as f:
                        f.write(review_content)
                    time.sleep(1)
                    if settings.DEBUG:
                        print("currentPage:",page)
                except Exception as e:
                    fail_page_que.put((review_url, key_word, atuple[0], page))
                    print(e)
        except Exception as e:
            print(e)
            continue


def extract_goods_from_tmall_page(HTML):
    """ return: (商品名称，价格，商品id-店铺id元组)"""
    from lxml import etree
    HTML = HTML.decode("utf-8","ignore")
    tree = etree.HTML(HTML)
    goods_warp = tree.xpath('//div[@class="product-iWrap"]')
    goods_list = []
    for g in goods_warp:
        goods_name = g.xpath('./div[@class="productTitle productTitle-spu"]/a[1]/text()')
        price = g.xpath('./p[@class="productPrice"]/em/text()')
        url = g.xpath('.//a[1]/@href')[0]
        pattern = re.compile('id=(?P<id>.*?)&.*?user_id=(?P<user_id>.*?)&', re.S) #r'<a href="//detail.tmall.com/item.htm?id=(?P<id>.*?)&.*?user_id=(?P<user_id>.*?)&
        goods_seller_tuple = re.findall(pattern, url)
        if goods_name:
            goods_list.append((goods_name[0], price[0], goods_seller_tuple[0]))
    return goods_list


def do_job(url, key_word, fail_page_que, spider_heart):
    global heart
    heart = spider_heart
    heart.goods_url = url
    heart.name = "TMALL"
    heart.category = key_word
    print("Tmall spider start!")
    if not url.startswith("https:"):
        url = "https:" + url
    content = render_js(url)
    goods_info_list = extract_goods_from_tmall_page(content)
    for item in goods_info_list:
        item_id = "TMALL_" + "-".join((item[2][1],item[2][0]))
        heart.current_goods_id = item_id
        title = item[0]
        platform = "TMALL"
        category = key_word
        detail = "{update: %s, price: %s}"%(time.strftime("%Y-%m-%d %H:%M:%S"), item[1]) 
        dataItem.Good(
            item_id=item_id, title=title, 
            platform=platform,
            category=category, 
            detail=detail).save_to_db()
    goods_seller_tuple_list = [i[2] for i in goods_info_list]
    if(len(goods_seller_tuple_list)==0):
        print(content)
    else:
        print("Get %d items in %s"%(len(goods_seller_tuple_list), url))
    heart.g_num = len(goods_seller_tuple_list)
    get_review_from_api(goods_seller_tuple_list, key_word, fail_page_que)