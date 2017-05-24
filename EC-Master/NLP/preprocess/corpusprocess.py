# coding:utf-8
# python 2
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import os
import json
import time
import pprint
import logging

import MySQLdb

import settings
import dataItem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='preprocess.log',
    filemode='w')

# Data base settings:
## Mysql
mysql_url = settings.mysql_url
ms_user = settings.ms_user
ms_pa = settings.ms_pa
ms_db = settings.ms_db

review_set = set()

def review_is_expected(review_body):
    # 长度筛选
    if len(review_body)<3:
        return False
    # 全字母数字筛选
    pattern1 = re.compile('^[a-zA-Z_0-9]+$', re.S)
    pattern2 = re.compile('^[\s+\.\!\/_,$%^*(+\"\']')
    pattern3 = re.compile('^[+——！，。？、~@#￥%……&*（）]')
    if re.findall(pattern1, review_body) or re.findall(pattern2, review_body) or re.findall(pattern3, review_body):
        print("Filter comment: " + review_body)
        return False
    return True



def distinct_sql_items():
    # 打开数据库连接
    db = MySQLdb.connect(host=mysql_url, user=ms_user, passwd=ms_pa, db=ms_db, port=3306, charset='utf8')
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    sql_str = "SELECT * FROM reviews.review_item where key_word='爽肤水';"
    cursor.execute(sql_str)
    items = cursor.fetchall()
    corpus = []
    # for i in range(len(items)):
    #   if items[i]
    for i in range(len(items)):
        review_body = items[i][2]
        if review_is_expected(review_body):
            item = dataItem.Review(items[i][0], items[i][1], items[i][2], items[i][3], str(items[i][4]), items[i][5], items[i][6], items[i][7])
            corpus.append(item.tans_to_dict())
    db.close()
    print(len(corpus))
    return corpus

if __name__ == "__main__":
    with open("shaungfushui_review.json", "w") as f:
        f.write(json.dumps(distinct_sql_items()))
    # distinct_sql_items()
    