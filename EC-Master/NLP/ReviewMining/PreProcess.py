# -*- coding: utf-8 -*-

""" 中文观点数据预处理：提取数据库中的评论内容，进行筛选操作剔除无用评论 """
# ----------------------------
# Author: Kun Liu         
# Start date: 2017-05-18
# Latest edit: 2017-05-18 
# -----------------------------

import re
import pymysql as MySQLdb
import settings

def query_comment_from_db(platform, num=0, by_category=False, cate_name=""):
    db = MySQLdb.connect(
        host=settings.MYSQL_DOMIN, 
        user=settings.MYSQL_USER, 
        passwd=settings.MYSQL_PA, 
        db=settings.MYSQL_DB, 
        port=3306, 
        charset='utf8'
    )
    cursor = db.cursor()
    comment_list = []
    if by_category:
        cursor.execute("select item_id from ec_goods where category=%s", (cate_name.encode("utf-8")))
        item_id_list = cursor.fetchall()
        print(len(item_id_list))
        if not num:
            for item_id in item_id_list:
                if cursor.execute('select content from ec_comment where item_id_id=%s', ( item_id )):
                    comment_list += cursor.fetchall()
                else:
                    continue
        else:
            for item_id in item_id_list:
                if cursor.execute('select content from ec_comment where item_id_id=%s limit %s', ( item_id, num )):
                    comment_list += cursor.fetchall()
                else:
                    continue

    else:
        if not num:
            if cursor.execute('select content from ec_comment where platform=%s', ( platform)):
                comment_list += cursor.fetchall()
        else:
            if cursor.execute('select content from ec_comment where platform=%s limit %s', ( platform, num )):
                comment_list += cursor.fetchall()
    db.close()
    print("Get %d item from db"%len(comment_list))
    return comment_list


def trim_cmt(cmt_list):
    import html.parser as HTMLParser
    html_parser = HTMLParser.HTMLParser()
    pattern = re.compile("<.*>.*?<.*>", re.S)
    return map(lambda x: re.sub(pattern, "", html_parser.unescape(x[0])).strip(), cmt_list)


def review_is_expected(review_body):
    # 长度筛选
    if len(review_body)<3:
        return False
    # 全字母数字筛选
    pattern1 = re.compile('^[a-zA-Z_0-9]+$', re.S)
    pattern2 = re.compile('^[\s+\.\!\/_,$%^*(+\"\']')
    pattern3 = re.compile('^[+——！，。？、~@#￥%……&*（）]')
    if re.findall(pattern1, review_body) or re.findall(pattern2, review_body) or re.findall(pattern3, review_body):
        print("Removed comment: " + review_body)
        return False
    return True


def get_review_corpus_by(platform, num=0, by_category=False, cate_name=""):
    return list(filter(review_is_expected, trim_cmt(query_comment_from_db(platform, num, by_category, cate_name))))

def main():
    for cmt in get_review_corpus_by(platform="TMALL"):
        print(cmt)


if __name__ == '__main__':
    main()