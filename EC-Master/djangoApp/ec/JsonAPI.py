# coding:utf-8

import os
from ec.ReviewMining import AspectAnalyse

def get_json_by(platform, cmt_num=0, by_category=False, cate_name="", k=20):
	json_dir = "ec/JsonCache"
	json_files = os.listdir(json_dir)
	json_name = "_".join((platform,str(k),str(cmt_num),str(by_category),cate_name))+".json"
	json_path = os.path.join(json_dir,json_name)
	if json_name in json_files:
		fr = open(json_path, "r")
		content = fr.read()
		fr.close()
		return content
	else:
		re_json = AspectAnalyse.get_aspect_json(platform=platform, cmt_num=cmt_num, by_category=by_category, cate_name=cate_name, k=k)
		with open(json_path, "w") as fw:
			fw.write(re_json)
		return re_json


def main():
	import pprint
	import json
	pprint.pprint(get_json_by("JD", cmt_num=100, by_category=True, cate_name="JD~电脑,办公~电脑整机~笔记本"))

if __name__ == '__main__':
	main()