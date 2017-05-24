# coding:utf-8
# ----------------------------
# Author: Kun Liu         
# Start date: 2017-05-16
# Latest edit: 2017-05-17
# -----------------------------
from __future__ import unicode_literals
from __future__ import division

""" 解析页面数据导入数据库 """

import re
import os
import json
import time
import datetime
import pprint
import logging
import pymysql as MySQLdb
import settings
from DataParser import dataItem


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='jsonToDataBase.log',
    filemode='a')


def is_item_in_db(item_id):
    db = MySQLdb.connect(
    host=settings.MYSQL_DOMIN, 
    user=settings.MYSQL_USER, 
    passwd=settings.MYSQL_PA, 
    db=settings.MYSQL_DB, 
    port=3306, 
    charset='utf8'
    )
    cursor = db.cursor()
    if cursor.execute("select 1 from ec_goods where item_id =%s",(item_id)):
        db.close()
        return True
    else:
        db.close()
        return False


def extract_goods_of_jd(json_path):
    platform = "JD"
    try:
        with open(json_path, "rb") as f:
            content = f.read().decode("UTF-8","ignore")
            pattern = re.compile("<div>.*?<div>", re.S)
            content = re.sub(pattern, "", content)
            revs = json.loads(content)
            cms = revs.get("comments","")
            if cms:
                title = cms[0]["referenceName"]
                # print(title)
            else:
                return False
            category = "~".join(json_path.split("\\")[-1].split("_")[0:-2])
            goods_id = "%s_%s"%(platform, str(revs["productCommentSummary"]["productId"]))
            item = dataItem.Good(item_id=goods_id, title=title, category=category, platform=platform, detail=revs.get("productAttr", "NULL")) # referenceName
            return item
    except Exception as e:
        print(e)


def extract_goods_of_tmall(json_path):
    platform = "TMALL"
    try:
        with open(json_path, "rb") as f:
            content = f.read().decode("UTF-8","ignore")
            pattern = re.compile("<div>.*?<div>", re.S)
            content = re.sub(pattern, "", content)
            revs = json.loads(content)
            cms = revs.get("comments","")
            if cms:
                title = cms[0]["referenceName"]
                # print(title)
            else:
                return False
            category = "~".join(json_path.split("\\")[-1].split("_")[0:-3])
            goods_id = "%s_%s"%(platform, str(revs["productCommentSummary"]["productId"]))
            item = dataItem.Good(item_id=goods_id, title=title, category=category, platform=platform, detail=revs.get("productAttr", "NULL")) # referenceName
            return item
    except Exception as e:
        print(e)


"""
    京东数据包含信息比较全面，适于用来做分析
"""     
def extract_comment_of_jd(json_path):
    items = []
    platform = "JD"
    try:
        with open(json_path, "rb") as f:
            # 京东的json文本需要清洗后才能用python 的 json正常导入获取python对象
            content = f.read().decode("GBK", "ignore")
            pattern = re.compile("<div>.*?<div>", re.S)
            content = re.sub(pattern, "", content)
            revs = json.loads(content.replace("\\","").replace("\r",""))
            if "productCommentSummary" not in revs:
                return
            goods_id = "%s_%s"%(platform, str(revs["productCommentSummary"]["productId"]))
            key_word = json_path.split("_")[-3]
            for rev in revs["comments"]:
                rev_id = platform + "_" + rev["referenceId"] + "_" + str(rev["id"])
                content = rev["content"]
                author = rev["nickname"]
                date = rev["creationTime"]
                rating = rev["score"]/5
                item = dataItem.Review(rev_id, 
                    item_id=goods_id, content=content, author=author, 
                    date=date, rating=rating, platform=platform)
                items.append(item)
    except Exception as e:
        print(json_path)
        print(e)
        logging.info("Bad json file of JD:" + json_path)
    return items


def extract_comment_of_tmall(json_path):
    """Extract comment of data from Tmall comment API .

    Args:
        json_path: the path of json_file 

    Returns:
        A list of Review-type. Each Review is an instance of dataItme.Review.
    Raises:
        Null
    """
    items = []
    platform = "TMALL"
    with open(json_path, "r") as f:
        content = f.read()
        try:
            revs = json.loads(content, encoding="utf-8")["rateDetail"]
            goods_id = json_path.split("_")[-2]
            key_word = json_path.split("_")[-3]
            for rev in revs["rateList"]:
                sellerId = rev["sellerId"]
                item_id = "TMALL_" + str(sellerId)  + "-" + goods_id
                rev_id = item_id +"_"+str(rev["id"])
                content = rev["rateContent"]
                author = rev["displayUserNick"]
                date = rev["rateDate"]
                rating = "-1"   
                item = dataItem.Review(rev_id=rev_id, item_id=item_id, content=content, author=author, date=date, rating=rating, platform=platform)
                # if settings.DEBUG:
                #     pprint.pprint(item.make_dict())  
                items.append(item)
            return items
        except Exception as e:
            if "anti_Spider" in content:
                print("天猫反爬虫页面:" + json_path)
                logging.info(json_path)
            else:
                print("解析失败文件%s"%json_path)
                print(str(e))


def init_db():
    creata_table_query = """
            CREATE TABLE IF NOT EXISTS ec_comment(
            id int(11),
            rev_id varchar(150) NOT NULL,
            item_id_id varchar(150) NOT NULL,
            content text NOT NULL,
            author varchar(150),
            date datetime NOT NULL,
            rating float,
            platform varchar(50) NOT NULL,
            PRIMARY KEY(id)
            )CHARSET=utf8
            """
    # 打开数据库连接
    db = MySQLdb.connect(host=settings.MYSQL_DOMIN, user=settings.MYSQL_USER, 
        passwd=settings.MYSQL_PA, db=settings.MYSQL_DB, port=3306, charset='utf8')
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute(creata_table_query)
    # 使用 fetchone() 方法获取一条数据库。
    data = cursor.fetchone()
    print("Database version : %s " % data)


def pip_goods_to_mysql(goods_list):
    OK = True
    if not goods_list:
        return False
    db = MySQLdb.connect(host=settings.MYSQL_DOMIN, user=settings.MYSQL_USER, 
        passwd=settings.MYSQL_PA, db=settings.MYSQL_DB, port=3306, charset='utf8')
    cursor = db.cursor()
    for goods in goods_list:
        if not goods:
            continue
        if cursor.execute("select 1 from ec_goods where item_id =%s",(goods.item_id)):
            continue
        cursor.execute("""INSERT INTO ec_goods (item_id,title,platform,category,detail)
                        VALUES
                        (%s, %s, %s, %s, %s);""",(goods.item_id, 
                        goods.title, goods.platform,
                        goods.category, "{update: %s}"%str(datetime.datetime.today())))
    db.commit()
    db.close()
    return OK
    

def pip_comment_to_mysql(items):
    OK_FLAG = True
    db = MySQLdb.connect(host=settings.MYSQL_DOMIN, user=settings.MYSQL_USER, passwd=settings.MYSQL_PA, db=settings.MYSQL_DB, port=3306, charset='utf8')
    cursor = db.cursor()
    if not items:
        return False
    for item in items:
        i = item.make_dict()
        if cursor.execute("select 1 from ec_comment where rev_id =%s",(i["rev_id"])):
            continue
        # item 数据编码要求为 utf-8 !!!
        cmt_content = i["content"].strip().encode("utf-8")
        try:
            cursor.execute("""INSERT INTO ec_comment (rev_id,item_id_id,content,author,date,rating,platform)
                            VALUES
                            (%s, %s, %s, %s, %s, %s, %s);""",(i["rev_id"], 
                            i["item_id"], cmt_content,
                            i["author"], i["date"], 
                            i["rating"], i["platform"]))
        except Exception as e:
            # try:
            #     cursor.execute("""INSERT INTO ec_comment (rev_id,item_id_id,content,author,date,rating,platform) 
            #                     VALUES 
            #                     (%s, %s, %s, %s, %s, %s, %s);""",(
            #                         i["rev_id"], 
            #                         i["item_id"], i["content"].encode("utf-8"),
            #                         i["author"].encode("utf-8"), i["date"], i["rating"], 
            #                         i["platform"].encode("utf-8")) )
            # logging.error(str(e) + " 向数据库导入数据时出现意外的编码错误.")
            print(str(e) + " 向数据库导入数据时出现意外的编码错误.")
            # pprint.pprint(i)
            OK_FLAG = False  
    # 关闭数据库连接
    db.commit()
    db.close()
    return OK_FLAG


def walk_dir_get_file_path(dir_path):
    file_list = []
    for root, dirs, files in os.walk(dir_path):#递归path下所有目录
        for f_name in files:
            if f_name.lower().endswith('.json'):
                path_dst = os.path.join(root,f_name)
                file_list.append(path_dst)
    return file_list


def load_json_from_dir_to_mdb(dir_path):
    json_list = walk_dir_get_file_path(dir_path)
    print("%d json found"%len(json_list))
    goods_list = []
    ok_count = 0
    goods_list = []
    for path in json_list:
        if "TMALL" in path:
            goods_list.append(extract_goods_of_tmall(path))
        elif "JD" in path:
            goods_list.append(extract_goods_of_jd(path))
        else:
            pass
    if pip_goods_to_mysql(goods_list):
        print("Load goods info success!")

    for path in json_list:
        if "TMALL" in path:
            cmt = extract_comment_of_tmall(path)
        elif "JD" in path:
            cmt = extract_comment_of_jd(path)
        else:
               pass
        if pip_comment_to_mysql(cmt):
            ok_count += 1
    print("Load %d json file success!"%ok_count)
