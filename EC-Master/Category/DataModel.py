# -*- coding: utf-8 -*-

# ----------------------------
# Author: Kun Liu         
# Start date: 2017-05-03
# Latest edit: 2017-05-07
# -----------------------------

# -----Python 3 Compatible
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals
# ---------------------------------

__version__ = "1.1"

import pprint

class Node:
    def __init__(self, name, website):
        self.name = name
        self.website = website

    def get_name(self):
        return self.name

    def get_website(self):
        return self.website

    def make_dic(self):
        pass

class CateLV_1(Node):
    """ 一级目录节点 """
    def __init__(self, name, website, lv2_list=[], lv3_list=[]):
        self.name = name
        self.website = website
        self.lv2_list = lv2_list
        self.lv3_list = lv3_list

    def make_dic(self):
        return {"lv1_name":self.name, "lv2_list":[i.make_child_tree() for i in self.lv2_list] ,"web":self.website}

    def make_tree(self):
        return {"name":self.name, "children":[i.make_tree() for i in self.lv2_list]}

    def show_child_tree(self):
        pprint.pprint(self.make_dic())

    def get_level(self):
        return 1


class CateLV_2(Node):
    """ 二级目录节点 """
    def __init__(self, name, lv1, lv3_list = []):
        super(CateLV_2, self).__init__(name, lv1.website)
        # self.name = name
        # self.website = lv1.website
        self.lv1 = lv1
        self.lv3_list = lv3_list

    def make_dic(self):
        return {"lv1_name":self.lv1.name, "lv2_name":self.name, "lv3_list":[(i.name, i.url) for i in self.lv3_list], "web":self.website}

    def make_tree(self):
        return {"name":self.name, "children":[{"name":i.name, "url":i.url} for i in self.lv3_list]}

    def show_child_tree(self):
        pprint.pprint({"web":self.website, "lv2_name":self.name, "lv3_list":self.lv3_list})

    def make_child_tree(self):
        return {"lv2_name":self.name, "lv3_list":[(i.name, i.url) for i in self.lv3_list]}
    
    def get_level(self):
        return 2


class CateLV_3(Node):
    """ 三级目录节点 """
    def __init__(self, name, url, lv2):
        super(CateLV_3, self).__init__(name, lv2.website)
        self.lv2 = lv2
        self.url = url
        self.cate_str = '{web}_{lv1}_{lv2}_{lv3}'.format(web=self.website, lv1=self.lv2.lv1.name,
                                                lv2=self.lv2.name, lv3=self.name)
    def make_dic(self):
        return {"web":self.website, "lv1":self.lv2.lv1, "lv2":self.lv2, "lv3_name":self.name}

    def show_child_tree(self):
        pprint.pprint({"web":self.website, "lv3_name":self.name, "url":self.url})

    def get_level(self):
        return 3

    def __str__(self):
        return self.cate_str


# Usage: 简单测试
def test():
    nd_1 = CateLV_1("一级目录", "天猫")
    nd_2 = CateLV_2("二级目录", nd_1)
    nd_3 = CateLV_3("三级目录", "http://exam.ple", nd_2)
    nd_1.make_dic()
    nd_1.show_child_tree()
    nd_2.make_dic()
    nd_2.show_child_tree()
    nd_3.make_dic()
    nd_3.show_child_tree()
