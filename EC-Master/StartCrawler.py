# -*- coding: utf-8 -*-
# ----------------------------
# Author: Kun Liu         
# Start date: 2017-05-08
# Latest edit: 2017-05-16 
# -----------------------------

import urllib
import threading
import queue
from WebCrawler.spiders import amazonSpider as AMZ
from WebCrawler.spiders import jdSpider as JD
from WebCrawler.spiders import tmallSpider as TMALL
from WebCrawler.spiders import spareSpider as BEITAI
from WebCrawler.spiderHeart import SpiderHeart
from Category import CategoryApi

__python__ = 3.6

# 按关键字抓取方法
# def walk_by_keywords():
#     THREADS_LIST = []
#     fail_pages_que = queue.Queue()
#     for key in key_words:
#         x = urllib.parse.quote(key.encode("utf-8"))
#         jd_base_url = "http://search.jd.com/Search?keyword=%s&enc=utf-8"%x
#         tmall_base_url = "https://list.tmall.com/search_product.htm?q=%s&type=p"%x
#         amazon_base_url = "https://www.amazon.cn/s/&field-keywords=%s"%x
#         THREADS_LIST.append(threading.Thread(target = JD.do_job, args = (jd_base_url, key, fail_pages_que), name = 'jd'))
#         # THREADS_LIST.append(threading.Thread(target = TMALL.do_job, args = (tmall_base_url, key, fail_pages_que), name = 'tmall'))
#         # THREADS_LIST.append(threading.Thread(target = AMZ.do_job, args = (amazon_base_url, key), name = 'amazon'))
#         THREADS_LIST.append(threading.Thread(target = BEITAI.handle_failure, args = (jd_base_url, key, fail_pages_que), name = 'spareSpider'))
#         if settings.debug_mode:
#             print(jd_base_url)
#             print(tmall_base_url)
#             print(amazon_base_url)
#     for t in THREADS_LIST:
#         t.start()
#         t.join()
#     print("所有线程结束了")


THREADS_LIST = []  # 各个网站正常抓取的作业队列
def listen(heart_list):
    for heart in heart_list:
        heart.beat()
    if not list(filter(lambda x:x.is_alive(), THREADS_LIST)):
        print("Stoped")
        return
    threading.Timer(10.0, listen, (heart_list,)).start()


def walk_by_category(node_lv3, fail_pages_que):
    website = node_lv3.website
    global THREADS_LIST
    heart_list = []
    if website == "JD":
        heart = SpiderHeart(spider_name="JD")
        heart_list.append(heart)
        t = threading.Thread(
            target=JD.do_job,
            args=(node_lv3.url, node_lv3.cate_str, fail_pages_que, heart), 
            name='JD'
        )
        THREADS_LIST.append(t)
    elif website == "TMALL":
        heart = SpiderHeart(spider_name="TMALL")
        heart_list.append(heart)
        t = threading.Thread(
            target=TMALL.do_job,
            args=(node_lv3.url, node_lv3.cate_str, fail_pages_que, heart), 
            name='TMALL'
        )
        THREADS_LIST.append(t)
    elif website == "AMZ":
        heart = SpiderHeart(spider_name="AMZ")
        heart_list.append(heart)
        t = threading.Thread(
            target=AMZ.do_job,
            args=(node_lv3.url, node_lv3.cate_str, fail_pages_que, heart), 
            name='Amazon_Walker'
        )
        THREADS_LIST.append(t)
    t.start()
    listen(heart_list)



def start_walker(nodes_list=[]):
    walker_list = []
    fail_pages_que = queue.Queue()
    while nodes_list:
        node = nodes_list.pop()
        walker_list.append(threading.Thread(target = walk_by_category, args = (node, fail_pages_que), name = 'walker_%s'%node.website))
        walker_list.append(threading.Thread(target = BEITAI.handle_failure, args = (fail_pages_que,), name = "spareSpider"))
    for t in walker_list:
        t.start()


def init_cache_database():
    from WebCrawler import webdriver as wb
    wb.create_table_in_mysql()


def main():
    category_nodes = CategoryApi.get_level_3_nodes(
       website="TMALL", num=1, all=False, by_level2_node=True, node_name="电脑整机")
    category_nodes += CategoryApi.get_level_3_nodes(website="JD", all=False, num=1, by_level2_node=True, node_name="电脑整机")
    start_walker(category_nodes)
    # for node in category_nodes:
    #   print(node.url)
      # walk_by_category(node)


if __name__ == '__main__':
    main()

