# coding:utf-8
# ----------------------------
# Author: Kun Liu         
# Start date: 2017-05-16
# Latest edit: 2017-05-17 
# -----------------------------
from __future__ import unicode_literals
from __future__ import division

""" 商品及评论数据模型 """

import pymysql as MySQLdb
import settings

class ReviewRating:
    """
        rating value:评分
        best_rating:评分上限
        worst_rating:评分下限
    """
    def __init__(self, rating_value, best_rating, worst_rating):
        self.rating_value = rating_value
        self.best_rating = best_rating
        self.worst_rating = worst_rating

    def normalize(self):
        return self.rating_value/(self.best_rating - self.worst_rating)


class Review:
    def __init__(self, rev_id, item_id, content, author, date, rating, platform):
        self.rev_id = rev_id
        self.item_id = item_id
        self.content = content
        self.author = author
        self.date = date
        self.rating = rating
        self.platform = platform
        
    def make_dict(self):
        item_dict = {
        "rev_id":self.rev_id, "item_id":str(self.item_id),
        "content":self.content,
        "author":self.author, "date":self.date, 
        "rating":str(self.rating), "platform":self.platform, 
        }
        return item_dict


class Good:
    def __init__(self, item_id:str, title:str, platform:str, category, detail:str):
        self.item_id = item_id
        self.title = title
        self.category = category
        self.platform = platform
        self.detail = detail

    def save_to_db(self):
            db = MySQLdb.connect(
                host=settings.MYSQL_DOMIN, 
                user=settings.MYSQL_USER, 
                passwd=settings.MYSQL_PA, 
                db=settings.MYSQL_DB, 
                port=3306, 
                charset='utf8'
            )
            cursor = db.cursor()
            if cursor.execute("select 1 from ec_goods where item_id =%s",(self.item_id)):
                return
            cursor.execute("""INSERT INTO ec_goods (item_id,title,platform,category,detail)
                            VALUES
                            (%s, %s, %s, %s, %s);""",(self.item_id, 
                            self.title, self.platform,
                            self.category, self.detail)
            )
            db.commit()
            db.close()
            if settings.DEBUG:
                print("SssS!")