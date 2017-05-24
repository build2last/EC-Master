# -*- coding: utf-8 -*-
__python__ = 3.6

""" 中文观点挖掘：对评论进行分词、统计，提取出热门属性及相关评论 """
# ----------------------------
# Author: liukun       
# Start date: 2017-05-18
# Latest edit: 2017-05-18 
# Email: lancelotdev@163.com
# -----------------------------

import re
from ec.ReviewMining import PreProcess
from ec.ReviewMining import settings


def cut_comments_to_words(comment_corpus:list):
    """ 对评论进行分词，返回单词列表迭代器
    """
    import jieba
    with open("电商评论补充词典.txt", "r", encoding='utf-8') as f:
            for line in f:
                key_words = line.split(" ")[0]
                jieba.add_word(key_words)
    words_list = []
    for item in comment_corpus:
        words_list += jieba.lcut(item)
    return words_list


# 单词筛选
def words_filter(x):
    return (x not in open("中文停用词表_1208个.txt", encoding="utf-8").readlines()) and len(x) > 2


# 使用 NLTK 提取出现频率高的中文词汇
def top_k_fre_of(cmt_corpus, k=20):
    import nltk
    words_list = list( filter(words_filter, cut_comments_to_words(cmt_corpus)) )
    fdist = nltk.FreqDist(words_list)
    print("Words number [%d] in the words list"%fdist.N())
    top_words = sorted(fdist.keys(), key=lambda x:-fdist[x])
    out_put_file_name = "Top_k_fre_out.txt"
    with open(out_put_file_name, "w") as fw:
        for words in top_words[:k]:
            fw.write(words + " " + str(fdist[words]/fdist.N()) + "\n")
    return top_words[:k]


# 使用 jieba 基于 TF-IDF 算法的关键词抽取
def tf_idf_topk(cmt_corpus, k=20):
    import jieba.analyse
    content = ""
    for cmt in cmt_corpus:
        content += cmt
    top_words = jieba.analyse.extract_tags(content, topK=k)
    out_put_file_name = "TF-IDF_out.txt"
    with open(out_put_file_name, "w") as fw:
        for words in top_words[:k]:
            fw.write(words + "\n")
    return top_words[:k]


def cut_ch_sentence(sentence):
    import re
    pa = re.compile('[，。！；~、？（）]', re.S)
    se_list = re.split(pa, sentence)
    return se_list


def top_k_words_of(platform, k=20, cmt_num=0, by_category=False, cate_name="", show_cmt_of_words=False):
    cmt_corpus = PreProcess.get_review_corpus_by(
        platform=platform, num=cmt_num,
        by_category=by_category,cate_name=cate_name
    )
    tpk_words1 = top_k_fre_of(cmt_corpus, k=20)
    tpk_words2 = tf_idf_topk(cmt_corpus, k=20)
    if show_cmt_of_words:
        sentence_list = []
        for cmt in cmt_corpus:
            sentence_list += cut_ch_sentence(cmt)
        from collections import defaultdict
        words_comment_dir1 = defaultdict(list)
        wc_dir2 = defaultdict(list)
        for words in tpk_words1:
            for sentence in filter(lambda sent:words in sent, sentence_list):
                words_comment_dir1[words].append(sentence)
        for words in tpk_words2:
            for sentence in filter(lambda sent:words in sent, sentence_list):
                wc_dir2[words].append(sentence)
        for key in words_comment_dir1.keys():
            print("------------------%s------------------\n"%key, words_comment_dir1[key], "\n")
        print("=========================================")
        for key in wc_dir2.keys():
            print("-------------------%s------------------\n"%key, wc_dir2[key], "\n")


# def key_words_file_compare(main_sample, compare_sample):
#     list1 = []
#     list2 = []
#     with open(main_sample,"r",encoding='utf-8') as fr:
#         for line in fr:
#             list1.append(line.split(' ')[0])
#     with open(compare_sample,"r") as fr:
#         for line in fr:
#             list2.append(line.split(' ')[0])
#     for i in list2:
#         if i in list1:
#             list1.remove(i)
#     for i in list1:
#         print(i)


def get_aspect_json(platform, cmt_num=0, by_category=False, cate_name="", k=20):
    import json
    cmt_corpus = PreProcess.get_review_corpus_by(
        platform=platform, num=cmt_num,
        by_category=by_category, cate_name=cate_name
    )
    tpk_words = tf_idf_topk(cmt_corpus, k=20)
    sentence_list = []
    for cmt in cmt_corpus:
        sentence_list += cut_ch_sentence(cmt)
    words_tree = dict()
    words_tree["name"] = cate_name
    words_tree["children"] = []
    for words in tpk_words:
        comment_dic = dict()
        comment_dic["children"] = []
        comment_dic["name"] = words
        for sentence in list(filter(lambda sent:words in sent, sentence_list))[:10]:
            comment_dic["children"].append({"name":sentence})
        words_tree["children"].append(comment_dic)
    return json.dumps(words_tree)


def test_topk():
    import pprint
    pprint.pprint(get_aspect_json("JD", cmt_num=100, by_category=True, cate_name="JD~电脑,办公~电脑整机~笔记本"))


def main():
    test_topk()


if __name__ == '__main__':
    main()
