# coding:utf-8

from __future__ import division
from lxml import etree

# HTML expected to be UTF-8 file
def get_tree_node(HTML):
    import pprint
    tree = etree.HTML(HTML)
    level1_nodes = tree.xpath('//*[@class="normal-nav clearfix"]/li')
    level1_cates = []
    for node in level1_nodes:
        level1_cates.append(",".join(node.xpath('.//a/text()')))
    second_cate_root = tree.xpath('//*[@class="pannel-con j_CategoryMenuPannel"]')
    level2_cates = []
    for i in range(len(second_cate_root)):
        node = second_cate_root[i]
        level2_nodes = node.xpath('.//*[@class="hot-word-line"]')
        for node in level2_nodes:
            level2_name = node.xpath('.//div[@class="title-text"]/text()')
            third_cates_names = node.xpath('./*[@class="line-con"]/a/text()')
            third_cates_links = node.xpath('./*[@class="line-con"]/a/@href')
            third_cates_list = list(zip(third_cates_names, third_cates_links))
            if level2_name:
                second_cate_node = {"level1":level1_cates[i], "level2":level2_name[0], "level3":third_cates_list}
                level2_cates.append(second_cate_node)
                # pprint.pprint(second_cate_node)
    return level2_cates

def get_nodes(HTML_path="Category/HomePageParser/TmallHomePage.html"):
    HTML = open(HTML_path, "rb").read()
    return get_tree_node(HTML)

def test():
    import pprint
    path = "TmallHomePage.html"
    print(len(get_nodes(path)))
    # for node in get_nodes(path):
    #     pprint.pprint(node)