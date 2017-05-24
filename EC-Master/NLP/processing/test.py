# -*- coding: utf-8 -*-
#----------------------------
# Author: Kun Liu         
# Start date: 2017-03-20 
# Latest edit: 2017-03-20
# Email: lancelotdev@163.com
#=============================
# NLP


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import nltk
import jieba


# 预处理，解决原始文本编码问题和特殊字符剔除及格式处理
def pre_process(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        content = content.strip()
        content = content.replace("\n".encode("utf-8"),"".encode("utf-8"))
        content = content.replace("\r".encode("utf-8"),"".encode("utf-8"))
        # content = 
        return content

def section_cut(section):
    section = pre_process(section)
    seg_list = jieba.lcut(section)
    return seg_list

def main():
    section_list = section_cut("story.txt")
    words_list = [i for i in section_list if len(i)>2]
    # for i,j in enumerate(words_list):
    #     print(i,j)
    # print(words_list)
    fdist = nltk.FreqDist(words_list)
    # 词汇高频递减
    words = sorted(fdist.keys(), key=lambda x:-fdist[x])
    for i in words[0:10]:
        print(i)

def test():
    import json
    import pprint
    comment = json.load(open("shaungfushui_review.json"))   
    with open("corpus.bsv", "w") as f:
        f.write("review||rating\n")
        for i in comment[:1000]:
            review = i["review_body"]
            if len(review)>6:
                f.write(review+"||"+i["review_rating"]+"\n")
            # pprint.pprint(i)


if __name__ == '__main__':
    # main()
    test()