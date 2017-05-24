# coding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__python_version__ = 2.7


def read_lines(file):
    item_list = []
    with open(file, "r") as fr:
        for line in file:
            item_list.append(line)
    return item_list

def remove_stop_words(stop_words_file, corpus_file):
    stop_words = read_lines(stop_words_file)
    words = corpus_file