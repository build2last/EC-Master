# -*- coding: utf-8 -*-

""" 提供供外部调用的 API 接口 """
# ----------------------------
# Author: Kun Liu         
# Start date: 2017-05-07
# Latest edit: 2017-05-07
# -----------------------------

__python__ = "3.6"

import pprint
from Category.DataModel import CateLV_1, CateLV_2, CateLV_3
from Category.HomePageParser import Amazon as AMZ
from Category.HomePageParser import JD
from Category.HomePageParser import Tmall as TMALL


def make_category_tree_from_nodes(website, lv2_nodes=""):
    """ 构建根节点为一级商品目录的目录树 """
    if website == "JD":
        lv2_nodes = JD.get_nodes()
    elif website == "TMALL":
        lv2_nodes = TMALL.get_nodes()
    elif website == "AMZ":
        lv2_nodes = AMZ.get_nodes()
    elif lv2_nodes=="":
        print("Not available website:%s"%website)
        return {}
    lv1_dict = dict()
    lv2_dict = dict()
    for node in lv2_nodes:
        if node["level1"] not in lv1_dict:
            lv1_dict[node["level1"]] = CateLV_1(node["level1"], website, lv2_list=[])
        else:
            continue
    for node in lv2_nodes:
        if node["level2"] not in lv2_dict:
            lv2_dict[node["level2"]] = CateLV_2(node["level2"], lv1_dict[node["level1"]], lv3_list=[])
        lv1_dict[node["level1"]].lv2_list.append(lv2_dict[node["level2"]])
        for lv3_node in node["level3"]:
            lv3_node = CateLV_3(lv3_node[0], lv3_node[1], lv2_dict[node["level2"]])
            lv2_dict[node["level2"]].lv3_list.append(lv3_node)
    return lv1_dict


def get_level_3_nodes(
        website, all=True, num=0, 
        by_level1_node=False, 
        by_level2_node=False, 
        node_name=" "):
    root_node = make_category_tree_from_nodes(website)
    level3_nodes = []
    if all and by_level1_node==False and by_level2_node==False:
        for item in root_node:
            for lv2_node in root_node[item].lv2_list:
                for lv3_node in lv2_node.lv3_list:
                    level3_nodes.append(lv3_node)
        if num:
            return level3_nodes[0:num]
        else:
            return level3_nodes
    elif by_level1_node and by_level2_node==False:
        if node_name not in root_node:
            print("Level_1 category not found!")
            return []
        for lv2_node in root_node[node_name].lv2_list:
            for lv3_node in lv2_node.lv3_list:
                level3_nodes.append(lv3_node)
        if num:
            return level3_nodes[0:num]
        else:
            return level3_nodes
    elif by_level2_node and all==False and by_level1_node==False:
        for item in root_node:
            for lv2_node in root_node[item].lv2_list:
                if node_name == lv2_node.name:
                    for lv3_node in lv2_node.lv3_list:
                        level3_nodes.append(lv3_node)
                    if num:
                        return level3_nodes[0:num]
                    else:
                        return level3_nodes
    if not level3_nodes:
        print("Node not found!")
        return []


def plant_tree(website, show=False):
    """ 存储全站目录树至本地! """
    node_tree = make_category_tree_from_nodes(website)
    tree_dir = {"name":website, "children":[]}
    for item in node_tree:
        tree_dir["children"].append(node_tree[item].make_tree())
    with open("%s_Cate_tree.json"%website, "w") as fw:
        import json
        fw.write(json.dumps(tree_dir))
    if show:
        pprint.pprint(tree_dir)


def plant_trees():
    plant_tree("JD")
    plant_tree("TMALL")
    plant_tree("AMZ")


# Usage
def test():
    jd_lv3_cate_list = get_level_3_nodes("JD")
    cate_list = get_level_3_nodes("TMALL")
    print(len(cate_list))
