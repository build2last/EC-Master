# coding:utf-8

""" 爬虫作业调度和多线程安排 """

from __future__ import unicode_literals
from __future__ import division

__python__ = "3.6"

import urllib
import threading

from spiders import jdSpider as JD
from spiders import tmallSpider as TMALL
from spiders import amazonSpider as AMZ
from WebCrawler import settings


"""
京东控制翻页子弹：&vt=2
亚马逊控制翻页字段：&page=2
天猫控制翻页字段：&s=1
"""
def walk_by_keywords():
    key_words = settings.keywords
    threads_list = []
    for key in key_words:
        x = urllib.parse.quote(key.encode("utf-8"))
        jd_base_url = "http://search.jd.com/Search?keyword=%s&enc=utf-8"%x
        tmall_base_url = "https://list.tmall.com/search_product.htm?q=%s&type=p"%x
        amazon_base_url = "https://www.amazon.cn/s/&field-keywords=%s"%x
        # threads_list.append(threading.Thread(target = JD.do_job, args = (jd_base_url, key), name = 'jd'))
        # threads_list.append(threading.Thread(target = TMALL.do_job, args = (tmall_base_url, key), name = 'tmall'))
        threads_list.append(threading.Thread(target = AMZ.do_job, args = (amazon_base_url, key), name = 'amazon'))
        if settings.debug_mode:
            print(jd_base_url)
            print(tmall_base_url)
            print(amazon_base_url)
    for t in threads_list:
        t.start()
        t.join()
    print("所有线程结束了")
    

if __name__ =="__main__":
    walk_by_keywords()