# coding:utf-8
# ----------------------------
# Author: Kun Liu         
# Start date: 2017-05-22
# Latest edit: 2017-05-22 
# -----------------------------

import time

class SpiderHeart:
    def __init__(self, spider_name="loading", category="loading", current_goods_id="loading", g_num=0, goods_url="loading", cmt_pages=0, g_index=0, cmt_index=0):
        self.name = spider_name
        self.category = category
        self.current_goods_id = current_goods_id
        self.goods_url = goods_url
        self.g_num = g_num
        self.g_index = g_index
        self.cmt_pages = cmt_pages
        self.cmt_index = cmt_index

    def beat(self):
        print("==============%s==============="%time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Spider: %s"%self.name)
        print("Category: %s"%self.category)
        print("Goods id: %s"%self.current_goods_id)
        print("Goods list page: %s"%self.goods_url)
        print("Crawling the [%d/%d] goods."%(self.g_index, self.g_num))
        print("Crawling the [%d/%d] pages of comments"%(self.cmt_index, self.cmt_pages))
        print("--------------------------------")



