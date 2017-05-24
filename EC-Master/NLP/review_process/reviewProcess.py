# -*- coding: utf-8 -*-
# ----------------------------
# Author: Kun Liu         
# Start date: 2017-03-20 
# Latest edit: 2017-03-20
# Email: lancelotdev@163.com
# =============================
# NLP


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import sys
import re


def read_lines(file):
    item_list = []
    with open(file, "r", encoding='utf-8') as fr:
        for line in fr:
            item_list.append(line.strip())
    return item_list


# 预处理，解决原始文本编码问题和特殊字符剔除及格式处理
def pre_process(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
        content = content.strip()
        content = content.replace("\n".encode("utf-8"),"".encode("utf-8"))
        content = content.replace("\r".encode("utf-8"),"".encode("utf-8"))
        # content = 
        return content

# 是否保留
def filter_func(x):
    english_pattern = re.compile("^\w*?$",re.S)
    match = re.findall(english_pattern, x)
    stop_words = read_lines("中文停用词表_1208个.txt")
    if x in stop_words:
        return False
    return len(x.strip())>2 and not match

def corpus_format(line):
    return line.split("||")[0]

# corpus 编码需为 utf-8
def cut_corpus_to_words(corpus_file):
    import jieba
    with open("中文电商评论补充词典.txt", "r", encoding='utf-8') as f:
            for line in f:
                key_words = line.split(" ")[0]
                jieba.add_word(key_words)
    words_list = []
    with open(corpus_file, "r", encoding="utf-8") as f:
         for i in f:
            item = corpus_format(i)
            words_list += jieba.lcut(item)
    words_list = filter(filter_func, words_list)
    return words_list


def make_nltk_freq(words_list):
    import nltk
    return nltk.FreqDist(words_list)


# 对所有评论进行分词分析词频
def make_top_k_fre(corpus_file, k=20):
    words_list = cut_corpus_to_words(corpus_file)
    fdist = make_nltk_freq(words_list)
    print(fdist.N())
    top_words = sorted(fdist.keys(), key=lambda x:-fdist[x])
    out_put_file_name = corpus_file.split('.')[0]+"_output.txt"
    with open(out_put_file_name, "w") as fw:
        for words in top_words[:k]:
            fw.write(words + " " + str(fdist[words]/fdist.N()) + "\n")


# 基于 TF-IDF 算法的关键词抽取
def tf_idf_topk(corpus_file,k=20):
    import jieba.analyse
    with open(corpus_file,"r", encoding='utf-8') as f:
        content = ""
        for line in f:
            content += corpus_format(line)
        top_words = jieba.analyse.extract_tags(content,topK=k)
    out_put_file_name = corpus_file.split('.')[0]+"_TFIDF.txt"
    with open(out_put_file_name, "w") as fw:
        for words in top_words[:k]:
            fw.write(words + "\n")


def key_words_file_compare(main_sample, compare_sample):
    list1 = []
    list2 = []
    with open(main_sample,"r",encoding='utf-8') as fr:
        for line in fr:
            list1.append(line.split(' ')[0])
    with open(compare_sample,"r") as fr:
        for line in fr:
            list2.append(line.split(' ')[0])
    for i in list2:
        if i in list1:
            list1.remove(i)
    for i in list1:
        print(i)

def cut_ch_sentence(sentence):
    import re
    pa = re.compile('[，。！；~、？（）]', re.S)
    se_list = re.split(pa, sentence)
    return se_list

"""
2. 情感定位
"""
def classify_words(wordDict):
    # (1) 情感词
    senList = read_lines('BosonNLP_sentiment_score.txt')
    senDict = defaultdict()
    for s in senList:
        try:
            senDict[s.split(' ')[0]] = s.split(' ')[1]
        except Exception as e:
            continue
    # (2) 否定词
    notList = read_lines('notDict.txt')
    # (3) 程度副词
    degreeList = read_lines('degreeDict.txt')
    degreeDict = defaultdict(int)
    for d in degreeList:
        try:
            degreeDict[d.split(',')[0]] = d.split(',')[1]
        except Exception as e:
            continue
    senWord = defaultdict(int)
    notWord = defaultdict(int)
    degreeWord = defaultdict(int)
    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    return senWord, notWord, degreeWord


def words_review_relate(words, corpus_file):
    words_node = {'key':words, 're_list':[]}
    with open(corpus_file, "r") as f:
        for line in f:
            line = corpus_format(line)
            if words not in line:
                continue
            else:
                sentence_list = filter(lambda x:words in x, cut_ch_sentence(line))
                words_node["re_list"] += sentence_list
    return words_node


if __name__ == '__main__':
    # tf-idf 提取关键词
    tf_idf_topk("corpus.data")
    tf_idf_topk("control_group.dat") # 参照组——爽肤水评论
    # 直接统计分析统计关键词
    make_top_k_fre(corpus_file="corpus.data")
    make_top_k_fre(corpus_file="control_group.dat")
    key_words_file_compare("result.txt", "controlgroup_result.txt")

    # 情感分析算法
    # words_dict = defaultdict(int)
    # words_list = cut_corpus_to_words(corpus_file="corpus.data")
    # for i in range(len(words_list)):
    #     words_dict[words_list[i]] = i
    # a,b,c = classify_words(words_dict)
    # import pprint
    # pprint.pprint(a)
    # pprint.pprint(b)
    # pprint.pprint(c)

    # words_node = words_review_relate("外观", corpus_file="corpus.data")
    # words_node = words_review_relate("续航", corpus_file="corpus.data")
    # for i in words_node['re_list']:
    #     print(i)