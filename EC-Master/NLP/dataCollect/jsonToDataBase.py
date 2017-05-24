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
import dataItem
import settings

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='jsonToDataBase.log',
	filemode='w')


class amazonDataFormat:
	# 于 2016年2月23日
	@staticmethod
	def date_time_format(date_published):
		date_str = date_published.replace("于 ", "").replace("年","-").replace("月","-").replace("日","")
		return date_str

	# 4.0 颗星，最多 5 颗星
	@staticmethod
	def rating_format(review_rating):
		return str(float(review_rating.split(' ')[0])/5)


"""
	tamllSweetLevel: 天猫会员等级
	天猫单条评论数据不包含打分信息，不方便用于监督学习
"""
def format_tmall_json(json_path):
	items = []
	with open(json_path, "r") as f:
		content = f.read()
		try:
			revs = json.loads(content, encoding="utf-8")["rateDetail"]
			# 路径名包含一些信息
			# "E:\\BISHE\\reviews_backup\\jd_%s_%s_%d.json"%(key_word,id,page)
			item_id = "tm" + json_path.split("_")[-2]
			key_word = json_path.split("_")[-3]
			for rev in revs["rateList"]:
				rev_id = "tm_" + str(rev["id"])
				review_body = rev["rateContent"]
				author = rev["displayUserNick"]
				date_published = rev["rateDate"]
				review_rating = "-1"
				publisher = rev["cmsSource"]
				item = dataItem.Review(rev_id, item_id, review_body, author, date_published, review_rating, publisher, key_word).tans_to_dict()
				if settings.debug_mode:
					pprint.pprint(item.tans_to_dict())	
				items.append(item)
			return items
		except Exception as e:
			if "anti_Spider" in content.decode("utf-8"):
				print("天猫反爬虫页面:" + json_path)
				logging.info(json_path)
			else:
				print(content)
				print(json_path)
				print(str(e))


"""
	京东数据包含信息比较全面，适于用来做分析
"""		
def format_jd_json(json_path):
	items = []
	try:
		with open(json_path, "r") as f:
			# 京东的json文本需要清洗后才能用python 的 json正常导入获取python对象
			pattern = re.compile("<div>.*?<div>", re.S)
			content = re.sub(pattern, "", f.read())
			revs = json.loads(content)
			item_id = "jd_" + str(revs["productCommentSummary"]["productId"])
			key_word = json_path.split("_")[-3]
			for rev in revs["comments"]:
				rev_id = "jd_" + rev["guid"]
				review_body = rev["content"]
				author = rev["nickname"]
				date_published = rev["creationTime"]
				review_rating = rev["score"]/5
				publisher = "京东"
				item = dataItem.Review(rev_id, item_id, review_body, author, date_published, review_rating, publisher, key_word).tans_to_dict()
				if settings.debug_mode:
					pprint.pprint(item)	
				items.append(item)
			return items
	except Exception as e:
		logging.info("Bad json file of jd:" + json_path)


# Data base settings:
## Mysql
mysql_url = settings.mysql_url
ms_user = settings.ms_user
ms_pa = settings.ms_pa
ms_db = settings.ms_db


def init_db():
	creata_table_query = """
			CREATE TABLE IF NOT EXISTS nlp_sample(
			review_id varchar(150) NOT NULL,
			item_id varchar(150) NOT NULL,
			review_body text NOT NULL,
			author varchar(150),
			date_published datetime NOT NULL,
			review_rating float,
			publisher varchar(100) NOT NULL,
			key_word varchar(100) NOT NULL,
			PRIMARY KEY(review_id)
			)CHARSET=utf8
			"""
	# 打开数据库连接
	db = MySQLdb.connect(host=mysql_url, user=ms_user, passwd=ms_pa, db=ms_db, port=3306, charset='utf8')
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 使用execute方法执行SQL语句
	cursor.execute(creata_table_query)
	# 使用 fetchone() 方法获取一条数据库。
	data = cursor.fetchone()
	print("Database version : %s " % data)


def pip_to_mysql(items):
	# 打开数据库连接
	db = MySQLdb.connect(host=mysql_url, user=ms_user, passwd=ms_pa, db=ms_db, port=3306, charset='utf8')
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 使用execute方法执行SQL语句
	# 插入
	if not items:
		return
	for i in items:
		if cursor.execute("select 1 from nlp_sample where review_id =%s",(i["review_id"])):
			continue
		insert_query = """INSERT INTO nlp_sample (review_id,item_id,review_body,author,
						date_published,review_rating,publisher, key_word) 
						VALUES 
						({review_id}, {item_id}, {review_body}, {author}, {date_published}, {review_rating}, {publisher}, {key_word});""".format(review_id = i["review_id"].encode("utf-8"), 
						item_id = i["item_id"].encode("utf-8"), review_body = i["review_body"],
						author = i["author"], date_published=i["date_published"], 
						review_rating = i["review_rating"], publisher=i["publisher"], key_word=i["key_word"])
		# item 数据编码要求为 utf-8 !!!
		try:
			cursor.execute("""INSERT INTO nlp_sample (review_id,item_id,review_body,author,
							date_published,review_rating,publisher, key_word) 
							VALUES 
							(%s, %s, %s, %s, %s, %s, %s, %s);""",(i["review_id"].encode("utf-8"), 
							i["item_id"].encode("utf-8"), i["review_body"],
							i["author"], i["date_published"], 
							i["review_rating"], i["publisher"], i["key_word"]))
		except Exception as e:
			try:
				cursor.execute("""INSERT INTO nlp_sample (review_id,item_id,review_body,author,
								date_published,review_rating,publisher,key_word) 
								VALUES 
								(%s, %s, %s, %s, %s, %s, %s, %s);""",(i["review_id"], 
								i["item_id"], i["review_body"].encode("utf-8"),
								i["author"], amazonDataFormat.date_time_format(i["date_published"]), 
								amazonDataFormat.rating_format(i["review_rating"]), i["publisher"].encode("utf-8"), i["key_word"]))
			except Exception as E:
				logging.error(str(E) + " 向数据库导入数据时出现意外的编码错误.")
				print(str(E)+ " 向数据库导入数据时出现意外的编码错误.")	
				print(insert_query)		
	# 关闭数据库连接
	db.commit()
	db.close()


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
	for path in json_list:
		try:
			items = []
			if "jd_" in path:
				items = format_jd_json(path)
			elif "tmall_" in path:
				items = format_tmall_json(path)
			elif "ama_" in path:
				with open(path, "r") as f:
					items = json.loads(f.read())
			if items:
				print("%d items added"%len(items))
				pip_to_mysql(items)
		except Exception as e:
			print("json装载错误："+ path)
			print(e)


if __name__ == "__main__":
	init_db()
	load_json_from_dir_to_mdb("Data")