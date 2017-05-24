# coding:utf-8
"""亚马逊电商评论页面解析"""

from __future__ import unicode_literals
from __future__ import division

__python_version__ = "3.6"

import re
import pprint
import time
import os
from lxml import etree
import WebCrawler.webdriver as wd
import settings


KEYWORD = ""


def driver_view(url):   
    driver.get(url)
    # 翻到底，详情加载
    js = "var q=document.documentElement.scrollTop=1000"
    driver.execute_script(js)
    content = driver.page_source
    if not content:
        time.sleep(3)
        content = driver.page_source
    return content


# 于 2016年2月23日
def date_time_format(date_published):
    date_str = date_published.replace("于 ", "").replace("年","-").replace("月","-").replace("日","")
    return date_str

# 4.0 颗星，最多 5 颗星
def rating_format(review_rating):
    return str(float(review_rating.split(' ')[0])/5)


def download_page_by_asin(asin):
    global KEYWORD 
    items = []
    review_url = "https://www.amazon.cn/product-reviews/" + asin
    review_page_content = driver_view(review_url)
    pat = re.compile('totalReviewCount">(.*?)</span>', re.S)
    re_count = int(re.findall(pat, review_page_content)[0])
    if settings.debug_mode:
        print("亚马逊：" + asin + " 商品共%d条评论待抓取."%re_count)
    review_page_count = (re_count+9)//10
    save_to = os.path.join(settings.json_dir_path, "AMZ_%s_p1.json"%asin)
    review_page_content = review_page_content.encode("utf-8")
    with open(save_to, "wb") as fw:
        fw.write(review_page_content)
    for page in range(2, review_page_count+1):
        item_url = "https://www.amazon.cn/dp/" + asin + "/&ie=UTF8/pageNumber=" + str(page)
        review_page_content = driver_view(item_url)
        save_to = os.path.join(settings.json_dir_path, "%s_p%d.json"%(asin,page))
        review_page_content = review_page_content.encode("utf-8")
        with open(save_to, "wb") as fw:
            fw.write(review_page_content)
    return items


def wander_page(base_url):
    content = driver_view(base_url)
    # content = wd.render_url_to_html(base_url, amazon_cookie)
    asin_pattern = re.compile('data-asin="(.*?)"', re.S)
    asin_list = re.findall(asin_pattern, content)
    items = []
    if settings.debug_mode:
        print("该页解析出亚马逊商品asin:")
        print(asin_list)
    for asin in asin_list:
        reviews = download_page_by_asin(asin)
        items += reviews
    driver.quit()
    return items

def do_job(url, key_word="ama_test"):
    global driver
    driver = wd.PHANTOMJS_driver()
    print("Amazon spider start")
    global KEYWORD 
    KEYWORD  = key_word
    wander_page(url)
    